from django.contrib import admin
from .models import *

admin.site.register([UserProfile, News, Comment, Photo, TrendingNews])

