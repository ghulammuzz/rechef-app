from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *
from account.models import Follow, Interest, User
from django.utils import timezone

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
class IngredientCoreModelForGetSerializer(serializers.ModelSerializer):
    recipe_fk = serializers.CharField(source = "recipe_fk.name", read_only=True)
    class Meta:
        model = Ingredient
        fields = ["id", "ingredient_text","recipe_fk", "quantity", "unit", "number", "note"]

class CoreIngredientModelForGetSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    ingredient = serializers.SerializerMethodField()
    
    def get_ingredient(self, obj):
        ingredient = Ingredient.objects.filter(core=obj)
        return IngredientCoreModelForGetSerializer(ingredient, many=True).data
    
    class Meta:
        model = Core
        fields = ["id", "name", "ingredient"]

class CategoryForListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    name = serializers.CharField(required=True)
    core = CoreIngredientModelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ["id", "name", "core"]

class CategoryModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    name = serializers.CharField(required=True)
    core = CoreIngredientModelSerializer(many=True)
    datas = serializers.SerializerMethodField()
    
    def get_datas(self, obj):
        
        # recipe category data
        core = Core.objects.filter(category_fk=obj)
        return CoreIngredientModelForGetSerializer(core, many=True).data
    
    class Meta:
        model = Category
        fields = ["id", "name", "core", "datas"]


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
    # interest = serializers.SerializerMethodField(read_only=False)
    interests = serializers.ListField(required=False)
    tag = serializers.SerializerMethodField()
    
    def get_tag(self, instance):
        return [item.interest for item in instance.interest.all()]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # manyrelated_manager
        # interest = representation['interest']
        # representation['interest'] = interest
        # Convert the difficulty to string

        
        # Convert the duration to hours and minutes
        duration = representation['duration']
        hours = duration // 60
        minutes = duration % 60
        representation['duration'] = f"{hours} Jam {minutes} menit"
        
        # method order by number
        method = representation['method']
        sorted_method = sorted(method, key=lambda k: k['number'])
        representation['method'] = sorted_method
        
        # show core ingredient in category
        category = representation['category']
        for core in category:
            core_ingredient = core['core']
            sorted_core = sorted(core_ingredient, key=lambda
                                    k: k['number'])
            core['core'] = sorted_core
            
        return representation

    def create(self, validated_data):
        
        categories = validated_data.pop('category', [])
        methods = validated_data.pop('method', [])
        interests = validated_data.pop('interests')
        creator = Recipe.objects.create(
            user = self.context['request'].user,
            created_at = timezone.now(),
            **validated_data
        )
        # ecxa
        # post data recipe with interest
        
        list_interest = []
        for interest in interests:
            get_interest = get_object_or_404(Interest, interest=interest)
            list_interest.append(get_interest)
        creator.interest.set(list_interest)   
            
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
        instance.is_hidden_like = validated_data.get('is_hidden_like', instance.is_hidden_like)
        instance.is_hidden_comment = validated_data.get('is_hidden_comment', instance.is_hidden_comment)
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
        
        interests = validated_data.pop('interests')
        list_interest = []
        for interest in interests:
            get_interest = get_object_or_404(Interest, interest=interest)
            list_interest.append(get_interest)
        instance.interest.set(list_interest)
        
        instance.method.all().delete()
        for method in methods:
            sub_method = Method.objects.create(recipe_fk=instance, **method)
            instance.method.add(sub_method)
            
        return super().update(instance, validated_data)
            
    class Meta:
        model = Recipe
        fields = ["id", "name", "user", "description", "image", "view", "fav", "duration", "portion", "calories", "difficulty", "is_hidden_like", "is_hidden_comment", "method", "category",
                  "interests", "tag"
                  ]
    
class RecipeModelForListSerializer(serializers.ModelSerializer):
    
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
    method = serializers.SerializerMethodField()
    
    def get_method(self, instance):
        # get 2 method and order by number
        methods = instance.method.all()
        sorted_method = sorted(methods, key=lambda k: k.number)
        method_2 = sorted_method[:2]
        return MethodModelSerializer(method_2, many=True).data
    
    def get_ingredient(self, instance):
        # get 2 ingredient
        ingredients = instance.ingredient.all()[:2]
        return IngredientCoreModelSerializer(ingredients, many=True).data 

            
    class Meta:
        model = Recipe
        fields = ["id", "name", "user", "description", "image", "view", "fav", "duration", "portion", "calories", "difficulty", "is_hidden_like", "is_hidden_comment", "method",]

class MyInfoViewSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(required=False)
    following = serializers.SerializerMethodField()
    follower = serializers.SerializerMethodField()

    
    def get_following(self, instance):
        data_following = Follow.objects.filter(following=instance).count()
        return data_following
    
    def get_follower(self, instance):
        data_follower = Follow.objects.filter(follower=instance).count()
        return data_follower
    
    class Meta:
        model = User
        fields = ['username', 'image', 'bio', 'following', 'follower',]
        
class IngredientByCategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Core
        fields = ["id", "name"]