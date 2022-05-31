from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=15)
    catid = models.IntegerField(default=0)
    #articles = models.ManyToManyField(Articles)
    def __str__(self):
        return self.name

class Articles(models.Model):
    title= models.CharField(default='NULL',max_length=100)
    content = models.CharField(default='NULL',max_length=1000000)
    writer = models.CharField(default='NULL',max_length=50)
    likes = models.PositiveIntegerField(default=0)
    cat = models.ManyToManyField(Category)
    pdate = models.DateTimeField(default=timezone.now)
    tags = models.CharField(default='NULL',max_length=700)        
    def __str__(self):
        return self.title


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=50)
    role = models.IntegerField()
    interests = models.ManyToManyField(Category)
    likes = models.ManyToManyField(Articles)
   # similar_users = models.ManyToManyField("self")
    def __str__(self):
        return self.fullName



