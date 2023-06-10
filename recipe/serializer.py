from rest_framework import serializers
from .models import Recipe

class PopularRecipeSerializer(serializers.ModelSerializer):
    
    def popular_recipe_pts(self, instance, view, like):
        ratio = (view * 1.75) + like
        return ratio    
    def search_recipe_pts(self, instance, search):
        pt = search * 2.5
        return pt
    class Meta:
        model = Recipe
        fields = "__all__"
        
class RecipeModelSerializer(serializers.Serializer):
    
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    image = serializers.ImageField(required=True, )

    def to_representation(self, instance):
        return super().to_representation(instance)    
    
    def create(self, validated_data):
        return Recipe.objects.create(
            user = self.context['request'].user,
            **validated_data
        )
    
    class Meta:
        model = Recipe
        fields = ["id", "name", "description", "image", "user", "view", "fav"]