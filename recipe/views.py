from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from permission.permission import isUserLogin
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializer import *

class DashboardView(generics.ListAPIView):
    permission_classes = (isUserLogin,)
    # serializer_class = PopularRecipeSerializer
    
class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeModelSerializer
    permission_classes = (isUserLogin,)
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]

    