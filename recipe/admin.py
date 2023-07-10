from django.contrib import admin
from .models import *

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image', 'user', 'view', 'fav', 'created_at')
    list_editable = ('view', 'user', 'fav')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_per_page = 25
admin.site.register(Recipe,  RecipeAdmin)

class MethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'method_text')
    list_display_links = ('id', 'method_text')
    search_fields = ('method_text',)
    list_per_page = 25
    
admin.site.register(Method,  MethodAdmin)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient_text', 'quantity', 'unit')
    list_display_links = ('id', 'ingredient_text')
    search_fields = ('ingredient_text',)
    list_per_page = 25
    
admin.site.register(Ingredient,  IngredientAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
admin.site.register(Category,  CategoryAdmin)

class CoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category_fk')
    
admin.site.register(Core,  CoreAdmin)