from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from account.serializer import InterestSerializer
from account.models import Interest
from .models import *
from .serializer import *
from pagination.pagination import ApiPagination
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
    
        popular = RecipeModelForListSerializer(sorted_recipe[:5], many=True)
        
        last_seen_data = request.user.last_view.all()
        reverse_last_seen_data = last_seen_data[::-1]
        last_seen = RecipeModelForListSerializer(reverse_last_seen_data[:5]  , many=True)
        
        return Response({
            "popular": popular.data,
            "last_seen": last_seen.data
        })
        
@method_decorator(ratelimit(key='ip', rate='1/s', block=True), name='dispatch')
class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeModelSerializer
    permission_classes = ()
    # parser_classes = (MultiPartParser, FormParser)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'user__username',
        'name',
        'category__name',
        'ingredient__ingredient_text',
        ]
    ordering_fields = ['user__username']

    pagination_class = ApiPagination

    def list(self, request, *args, **kwargs):
        self.pagination_class = ApiPagination
        self.serializer_class = RecipeModelForListSerializer
        # query_param for FEED
        type = request.query_params.get('type')
        page = self.paginate_queryset(self.queryset)
        if type == "all":
            print("all")
            page = self.paginate_queryset(self.queryset)
        elif type == "professional":
            page = self.paginate_queryset(self.queryset.filter(difficulty="Pro"))
        elif type == "newbie":
            page = self.paginate_queryset(self.queryset.filter(difficulty="Pemula"))
        elif type == 'new':
            print("new")
            page = self.paginate_queryset(self.queryset.order_by('-created_at'))

        serializer = RecipeModelForListSerializer(page, many=True)
        # return self.get_paginated_response(serializer.data)   
        return super().list(request, *args, **kwargs) 
         
    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.user != request.user:
            return Response({"message": "You are not allowed to delete this recipe."}, status=401)
        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        recipe = self.get_object()
        self.parser_classes = (MultiPartParser, FormParser)
        if recipe.user != request.user:
            print(request.user.username)
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
                request.user.last_view.add(recipe)
            else:
                recipe.view += 1
                recipe.guest.add(request.user)
                request.user.last_view.add(recipe)
                # recipe.updated_at = timezone.now()
                # max 5 in last view
        
            recipe.save()
        elif request.user == recipe.user:
            request.user.last_view.add(recipe)
        

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

class PaginationForRecipeCategoryView(ApiPagination):
    page_size = 13
    page_size_query_param = 'page_size'
    max_page_size = 1000

class RecipeCategoryView(generics.ListAPIView):
    permission_classes = ()
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    pagination_class = PaginationForRecipeCategoryView

class RecipeCategoryRetrieveView(generics.GenericAPIView):
    permission_classes = ()
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    pagination_class = PaginationForRecipeCategoryView
    
    def get(self, request, name_category):
        cat_id = get_object_or_404(Interest, interest=name_category)
        recipe = Recipe.objects.filter(interest=cat_id)
        serializer = RecipeModelForListSerializer(recipe, many=True)
        return Response(serializer.data)
    
class IngredientCategoryView(generics.GenericAPIView):
    permission_classes = ()
    queryset = Category.objects.all()
    serializer_class = CategoryForListSerializer
    
    def get(self, request, name_category):
        cat_id = get_object_or_404(Category, name=name_category)
        ingredient = Core.objects.filter(category_fk=cat_id)
        serializer = IngredientByCategorySerializer(ingredient, many=True)
        return Response(serializer.data)
    
class IngredientCategoryViewForList(generics.ListAPIView, generics.GenericAPIView):
    permission_classes = ()
    queryset = Category.objects.all()
    serializer_class = CategoryForListSerializer
    
class MyInfoView(generics.GenericAPIView):
    permission_classes = ()
    serializer_class = MyInfoViewSerializer
    
    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        # recipe = Recipe.objects.filter(user=user)
        serializer = MyInfoViewSerializer(user, many=False)
        
        # paginate in RecipeModelForListSerializer
        # paginate_view = 
        return Response(serializer.data)
    
class MyRecipeView(generics.ListAPIView):
    permission_classes = ()
    serializer_class = RecipeModelForListSerializer
    pagination_class = ApiPagination
    queryset = Recipe.objects.all()
    
    def list(self, request):
        user = get_object_or_404(User, username=request.user.username)
    
        # get 2 popular recipe
        recipe = Recipe.objects.filter(user=user)
        page = self.paginate_queryset(recipe)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
class IngredientView(generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = IngredientByCategorySerializer
    queryset = Core.objects.all()
    permission_classes = ()
