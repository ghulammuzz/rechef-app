from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipe-images/')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name