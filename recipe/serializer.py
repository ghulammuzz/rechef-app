from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *

class MethodModelSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    method_text = serializers.CharField(required=True)
    number = serializers.IntegerField(required=True)
    class Meta:
        model = Method
        fields = ["id", "number", "method_text"]


class IngredientCoreModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    quantity = serializers.FloatField(required=True)
    unit = serializers.ChoiceField(choices=Ingredient.Unit.choices, required=True)
    number = serializers.IntegerField(required=True)
    # recipe_fk = serializers.UUIDField(required=True)
    
    def create(self, validated_data):
        ingredient = Ingredient.objects.create(**validated_data)
        return ingredient
    
    class Meta:
        model = Ingredient
        fields = ["id", "ingredient_text", "quantity", "unit", "number", "note"]


class CoreIngredientModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    ingredient = IngredientCoreModelSerializer(many=False)
    
    def create(self, validated_data):
        core = Core.objects.create(**validated_data)
        return core
    
    class Meta:
        model = Core
        fields = ["id", "name", 'ingredient']

class CategoryModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    core = CoreIngredientModelSerializer(many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "core"]


class RecipeModelSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    # test
    image = serializers.ImageField(required=False)
    user = serializers.CharField(source = "user.username", read_only=True)
    duration = serializers.IntegerField(required=True)
    portion = serializers.IntegerField(required=True)
    calories = serializers.IntegerField(required=True)
    difficulty = serializers.ChoiceField(choices=Recipe.Difficulty.choices, required=True)
    method = MethodModelSerializer(many=True)
    category = CategoryModelSerializer(many=True)

    def get_method(self, obj):
        method = Method.objects.filter(recipe_fk=obj)
        sorted_method = method.order_by('number')
        return MethodModelSerializer(sorted_method, many=True).data
    
    def create(self, validated_data):
        
        categories = validated_data.pop('category', [])
        methods = validated_data.pop('method', [])
            
        creator = Recipe.objects.create(
            user = self.context['request'].user,
            **validated_data
        )
        for category in categories:
            name_category = category.pop('name')
            cores = category.get('core')
            get_category = get_object_or_404(Category, name=name_category)
            for core in cores:
                core_name = core.pop('name')
                ingredients = core.get('ingredient')
                        # get_or_create_core 
                core_data = Core.objects.filter(name=core_name).first()
                if core_data is None:
                    core_data = Core.objects.create(
                        name= core_name,
                        category_fk=get_category
                    )
                data_ingredients = Ingredient.objects.create(core=core_data, recipe_fk= creator, **ingredients)
                creator.ingredient.add(data_ingredients)
                
            creator.category.add(get_category)
            creator.save()
                
        for method in methods:
            sub_method = Method.objects.create(recipe_fk=creator, **method)
            creator.method.add(sub_method)
            
        return creator
    
    def update(self, instance, validated_data):
        
        categories = validated_data.pop('category', [])
        methods = validated_data.pop('method', [])
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.portion = validated_data.get('portion', instance.portion)
        instance.calories = validated_data.get('calories', instance.calories)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.save()
        
        for category in categories:
            name_category = category.pop('name')
            cores = category.get('core')
            get_category = get_object_or_404(Category, name=name_category)
            for core in cores:
                core_name = core.pop('name')
                ingredients = core.get('ingredient')
                        # get_or_create_core 
                core_data = Core.objects.filter(name=core_name, category_fk = get_category).first()
                if core_data is None:
                    core_data = Core.objects.create(
                        name= core_name,
                        category_fk=get_category
                    )
                data_ingredients = Ingredient.objects.filter(core=core_data, recipe_fk= instance).first()
                if data_ingredients is None:
                    data_ingredients = Ingredient.objects.create(core=core_data, recipe_fk= instance, **ingredients)
                else:
                    data_ingredients.quantity = ingredients.get('quantity')
                    data_ingredients.unit = ingredients.get('unit')
                    data_ingredients.number = ingredients.get('number')
                    data_ingredients.note = ingredients.get('note')
                    data_ingredients.save()
                    
                # data_ingredients, created = Ingredient.objects.update_or_create(core=core_data, recipe_fk= instance, **ingredients)
                # data_ingredients = Ingredient.objects.create(core=core_data, recipe_fk= instance, **ingredients)
                # instance.ingredient.all().delete()
                instance.ingredient.add(data_ingredients)
                
            instance.category.add(get_category)
            instance.save()
        
        instance.method.all().delete()
        for method in methods:
            sub_method = Method.objects.create(recipe_fk=instance, **method)
            instance.method.add(sub_method)
    #     instance.ingredient_fk.all().delete()
    #     for indgredient in indgredients:
    #         sub_indgredient = Ingredient.objects.create(recipe_fk=instance, **indgredient)
    #         instance.ingredient.add(sub_indgredient)
            
    #     instance.method_fk.all().delete()
    #     for method in methods:
    #         sub_method = Method.objects.create(recipe_fk=instance, **method)
    #         instance.method.add(sub_method)
            
        return super().update(instance, validated_data)
            
    class Meta:
        model = Recipe
        fields = ["id", "name", "user", "description", "image", "view", "fav", "duration", "portion", "calories", "difficulty", "method", "category"]
    
