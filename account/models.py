import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, gender, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        if not username:
            raise ValueError("Users must have an username")
        if gender is not None:
            user = self.model(
                username = username,
                email = self.normalize_email(email),
                gender = gender
            )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username = username,
            email = email,
            password = password,
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='user-profile/', blank=True, null=True)
    
    bio = models.TextField(blank=True, null=True)
    
    class Gender(models.TextChoices): 
        Unknown = 'Unknown', ('Unknown')
        Men = 'Men', ('Men')
        Women = 'Women', ('Women')
    
    gender = models.CharField(choices=Gender.choices, max_length=10, default=Gender.Unknown)
    interest = models.ManyToManyField('Interest')
       
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        
        if self.is_admin == True:
            return f"KING"
        else:
            return f"{self.email} - {self.username}"
        
class Interest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interest = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.interest