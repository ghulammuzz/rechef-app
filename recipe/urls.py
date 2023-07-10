from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'recipe'
router = DefaultRouter()

router.register(r'recipe', RecipeViewset, basename='recipe')

urlpatterns = [
    path(r'', include(router.urls)),
    path('favorite/', FavoriteView.as_view(), name='favorite-recipe'),
    path('dashboard/', DashboardView.as_view(), name='dashboard-viewww'),
    # path('recipe/', RecipeViewset.as_view(), name='recipe-detail'),
]
