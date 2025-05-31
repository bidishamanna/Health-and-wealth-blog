from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscriberOn = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.email
    
    