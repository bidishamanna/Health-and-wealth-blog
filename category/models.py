from django.db import models
# from account import User
from django.contrib.auth import get_user_model
# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=50,unique= True)
    description = models.CharField(max_length=500)
# Tracks which admin created each category
# This allows the system to track which admin added which category, especially useful if:
# There are multiple staff/admin users,You want to audit or filter categories by admin
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)



    def __str__(self) -> str:
        return self.name
    
    