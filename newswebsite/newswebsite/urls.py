from django.contrib import admin
from django.urls import path
from main.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', main_view, name='main'),
    path('', main_view, name='home'),
    path('politics/', politics_view, name='politics'),
    path('news/<int:news_id>/', news_template, name='news_template'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('newst/<int:news_id>/comment/', add_comment, name='add_comment'),
    path('tech/', tech_view, name='tech'),
    path('currency/', currency_view, name='currency'),
    path('culture/', culture_view, name='culture')
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)