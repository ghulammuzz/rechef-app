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
    
    def __str__(self):
        return self.name
    
class Method(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    method_text = models.TextField()
    
    def __str__(self):
        return self.method_text
    
class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ingredient_text = models.TextField()
    
    def __str__(self):
        return self.ingredient_text