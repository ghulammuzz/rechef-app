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

    path('recipe-category/', RecipeCategoryView.as_view(), name='recipe-category'),
    path('ingredient-category/', IngredientCategoryViewForList.as_view(), name='ingrediesasnt'),
    path('ingredient-category/<str:name_category>', IngredientCategoryView.as_view(), name='ingredient'),
    
    # path('ingredient/', IngredientView.as_view(), name='ingrediensssst'),
    
    path('my-info/', MyInfoView.as_view(), name='my-info'),
    path('my-recipe/', MyRecipeView.as_view(), name='my-recipe'),
]
