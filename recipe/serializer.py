from rest_framework import serializers
from .models import Recipe, Method, Ingredient

class MethodModelSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    method_text = serializers.CharField(required=True)
    number = serializers.IntegerField(required=True)
    class Meta:
        model = Method
        fields = ["id", "number", "method_text"]
        
class IngredientModelSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    ingredient_text = serializers.CharField(required=True)
    unit = serializers.ChoiceField(choices=Ingredient.Unit.choices, required=True)
    quantity = serializers.FloatField(required=True)
    number = serializers.IntegerField(required=True)
    class Meta:
        model = Ingredient
        fields = ["id", "number", "quantity", "unit", "ingredient_text"]
class RecipeModelSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    # test
    image = serializers.ImageField(required=False)
    
    duration = serializers.IntegerField(required=True)
    portion = serializers.IntegerField(required=True)
    calories = serializers.IntegerField(required=True)
    difficulty = serializers.ChoiceField(choices=Recipe.Difficulty.choices, required=True)
    method = MethodModelSerializer(many=True)
    ingredient = IngredientModelSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['method'] = instance.method_fk.all().order_by('number').values()
        data['ingredient'] = instance.ingredient_fk.all().order_by('number').values()
        return data


    def get_method(self, obj):
        method = Method.objects.filter(recipe_fk=obj)
        sorted_method = method.order_by('number')
        return MethodModelSerializer(sorted_method, many=True).data
    
    def create(self, validated_data):
        
        ingredients = validated_data.pop('ingredient', [])
        methods = validated_data.pop('method', [])
            
        creator = Recipe.objects.create(
            user = self.context['request'].user,
            **validated_data
        )
        for ingredient in ingredients:
            sub_ingredient = Ingredient.objects.create(recipe_fk=creator, **ingredient)
            creator.ingredient.add(sub_ingredient)
        
        for method in methods:
            sub_method = Method.objects.create(recipe_fk=creator, **method)
            creator.method.add(sub_method)
            
        return creator
    
    def update(self, instance, validated_data):
        indgredients = validated_data.pop('ingredient', [])
        methods = validated_data.pop('method', [])
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.portion = validated_data.get('portion', instance.portion)
        instance.calories = validated_data.get('calories', instance.calories)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.save()
        
        instance.ingredient_fk.all().delete()
        for indgredient in indgredients:
            sub_indgredient = Ingredient.objects.create(recipe_fk=instance, **indgredient)
            instance.ingredient.add(sub_indgredient)
            
        instance.method_fk.all().delete()
        for method in methods:
            sub_method = Method.objects.create(recipe_fk=instance, **method)
            instance.method.add(sub_method)
            
        return super().update(instance, validated_data)
            
    class Meta:
        model = Recipe
        fields = ["id", "name", "description", "image", "view", "fav", "duration", "portion", "calories", "difficulty", "method", "ingredient"]