from django.db import models
from category.models import Categories
from account.models import User

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    filename = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title    
    
