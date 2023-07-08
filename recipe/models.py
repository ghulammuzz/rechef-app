from django.db import models
import uuid

class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipe-images/')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    
    # aditional field
    duration = models.IntegerField(default=0)
    portion = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    
    # difficulty
    class Difficulty(models.TextChoices):
        Pemula = 'Pemula'
        Pro = 'Pro'
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)

    # method and ingredient
    method = models.ManyToManyField('Method')
    ingredient = models.ManyToManyField('Ingredient')
    
    # scalability issue
    view = models.IntegerField(default=0)
    fav = models.IntegerField(default=0)
    guest = models.ManyToManyField('account.User', related_name='guest', blank=True)
    
    # timestamp
    updated_at = models.DateTimeField(null=True, blank=True)
    
    # status
    class Status(models.TextChoices):
        Active = 'Active'
        Inactive = 'Inactive'
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.Active)
    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Core(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_fk = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='core_fk')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Method(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(default=0)
    recipe_fk = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='method_fk')
    method_text = models.TextField()
    
    def __str__(self):
        return self.method_text
    
class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ingredient_text = models.TextField()
    number = models.IntegerField(default=0)
    recipe_fk = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_fk')
    core = models.ForeignKey(Core, on_delete=models.CASCADE, related_name='ingredient_core')
    # unit
    class Unit(models.TextChoices):
        Q = 'Q'
        Gram = 'Gram'
        Liter = 'Liter'
        Sendok = 'Sendok'
        Buah = 'Buah'
        Sachet = 'Sachet'
        
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.Q)
    
    # quantity
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.ingredient_text
    
