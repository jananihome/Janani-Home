from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    app_name = models.CharField(max_length=200)
    comment= models.TextField()
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.author.username
