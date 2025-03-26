from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

    
class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=False)
    
    types_of_news = (('п', "Політика"), ("у", "Україна"), ("н", "Наука"), ("в", "Валюта"), ("к", "Кіно"))
    type_of_category = models.CharField(max_length=10, choices=types_of_news, default=None)
    
    date_of_publish = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.title

    

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment', blank=True, null=True)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=now)

    
    def __str__(self):
        return self.comment
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_DEFAULT, default=None, related_name='user')
    

class Photo(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='photo')
    image = models.ImageField(blank=True, null=True, default=None)


class TrendingNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='trending_news')
    
    
class Advertising(models.Model):
    image_a = models.ImageField(blank=False, default=None)
    image_b = models.ImageField(blank=False, default=None)
    