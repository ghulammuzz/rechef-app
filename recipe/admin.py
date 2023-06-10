from django.contrib import admin
from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image', 'user', 'view', 'fav')
    list_editable = ('view', 'fav')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_per_page = 25
admin.site.register(Recipe,  RecipeAdmin)
