from django.db import models
from django.contrib.auth.models import User

    

class Category(models.Model):
    name_category = models.CharField(max_length=40)
    image = models.ImageField()
    
    def __str__(self):
        return self.name_category
    
class News(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=None, related_name='category')
    
    types_of_news = (('п', "Політика"), ("у", "Україна"), ("н", "Наука"), ("в", "Валюта"), ("к", "Кіно"))
    type_of_category = models.CharField(max_length=10, choices=types_of_news, default=None)
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment', blank=True, null=True)
    comment = models.CharField(max_length=255)

    
    def __str__(self):
        return self.comment
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_DEFAULT, default=None, related_name='user')
    

class Photo(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='photo')
    image = models.ImageField(blank=True)
    
    