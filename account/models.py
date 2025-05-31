from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None  #disabling the default username field because using email as the unique identifier 
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    #password = models.CharField(max_length=100)


    USERNAME_FIELD = 'email'  #Tells Django to use email as the login field instead of the default username.
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=255, unique=True)           # Refresh Token
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email} (Expires: {self.expired_at})"


