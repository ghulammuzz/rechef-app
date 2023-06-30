from rest_framework import generics, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from permission.permission import isUserLogin
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializer import *

class DashboardView(generics.GenericAPIView):
    permission_classes = (isUserLogin)
    
    def get(self, request):
        user = request.user
        
        

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
        # increament view in recipe 
        # if owner view, not increament
        recipe = self.get_object()
        if recipe.user != request.user:
            recipe.view += 1
            recipe.save()
        return super().retrieve(request, *args, **kwargs)
