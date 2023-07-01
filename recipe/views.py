from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.utils import timezone
from permission.permission import isUserLogin
from .models import *
from .serializer import *

class DashboardView(generics.GenericAPIView):
    permission_classes = ()
    
    def get_point_populer(self, recipe):
        view = recipe.view
        fav = recipe.fav
        point = (view * 0.5) + (fav * 1)
        return point
    
    def get(self, request):
        recipe = Recipe.objects.all()
        sorted_recipe = sorted(recipe, key=self.get_point_populer, reverse=True)
        
        for i in range (len(sorted_recipe)):
            print(sorted_recipe[i].name, self.get_point_populer(sorted_recipe[i]))
        
        serializer = RecipeModelSerializer(sorted_recipe[:5], many=True)
        return Response(serializer.data)
        
@method_decorator(ratelimit(key='ip', rate='1/s', block=True), name='dispatch')
class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeModelSerializer
    permission_classes = ()
    # parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]

    def update(self, request, *args, **kwargs):
        recipe = self.get_object()
        self.parser_classes = (MultiPartParser, FormParser)
        if recipe.user != request.user:
            return Response({"message": "You are not allowed to update this recipe."}, status=401)
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        recipe = self.get_object()
               
        if recipe.user != request.user:
            len_viewed = len(request.user.last_view.all())
            if len_viewed == 5 or len_viewed > 5:
                request.user.last_view.remove(request.user.last_view.all()[0])
                request.user.last_view.add(recipe)
            elif len_viewed < 5:
                request.user.last_view.add(recipe)
            if recipe.guest.filter(id=request.user.id).exists():
                recipe.view += 0
            else:
                recipe.view += 1
                recipe.guest.add(request.user)
                # recipe.updated_at = timezone.now()
                # max 5 in last view
                
            recipe.save()
        
        # if recipe.user != request.user:
        #     recipe.view += 1
        #     # recipe.updated_at = timezone.now()
        #     # max 5 in last view
        #     len_viewed = len(request.user.viewed.all())
        #     if len_viewed == 5 or len_viewed > 5:
        #         request.user.viewed.remove(request.user.viewed.all()[0])
        #     request.user.viewed.add(recipe)
        #     recipe.save()
        return super().retrieve(request, *args, **kwargs)
    

@method_decorator(ratelimit(key='ip', rate='1/s', block=True), name='dispatch')
class FavoriteView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = ()
    queryset = Recipe.objects.all()
    serializer_class = RecipeModelSerializer
    
    def list(self, request):
        user = request.user
        user_fav = user.favorite.all()
        serializer = RecipeModelSerializer(user_fav, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        recipe_id = request.data.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if recipe in user.favorite.all():
            recipe.fav -= 1
            user.favorite.remove(recipe)
            recipe.save()
            return Response({"message": "removed"}, status=200)
        elif recipe not in user.favorite.all():
            recipe.fav += 1
            user.favorite.add(recipe)
            recipe.save()
            return Response({"message": "added"}, status=200)
