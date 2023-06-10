from django.db import models
import uuid

class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipe-images/')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    
    # scalability issue
    view = models.IntegerField(default=0)
    fav = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name