from django.http import HttpRequest
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.translation import gettext as _
import requests
import os

from dotenv import load_dotenv

load_dotenv()


def main_view(request):
    category_list = Category.objects.all()
    news_list = News.objects.all()
    images = Photo.objects.all()
    trending_news = TrendingNews.objects.select_related('news').order_by('-news__date_of_publish')[:5]

    
    url = os.getenv('url')
    response = requests.get(url)
    
    
    if response.status_code == 200:
        data_main = response.json()
        
        data = data_main['data']['stats']
        
        units = data['personnel_units']
        tanks = data['tanks']
        armoured_vehicles = data['armoured_fighting_vehicles']
        artillery = data['artillery_systems']
        mlrs = data['mlrs']
        planes = data['planes']
        helicopters = data['helicopters']
        fuel_tanks = data['vehicles_fuel_tanks']
        warships = data['warships_cutters']
        
    else:
        return f'Помилка доступу до серверу. Код: {response.status_code}'
    
    context = {
        "category": category_list,
        "news": news_list,
        "photo": images,
        'user': request.user,
        'trend': trending_news,
        
        'units': units,
        'tanks': tanks,
        'arm_veh': armoured_vehicles,
        'artillery': artillery,
        'mlrs': mlrs,
        'planes': planes,
        'helicopters': helicopters,
        'fuel_tanks': fuel_tanks,
        'warships': warships
    }
    
    return render(request, 'main/index.html', context)


def news_template(request, news_id):
    news = get_object_or_404(News, id=news_id)
    image = Photo.objects.filter(news=news)
    catebory_list = Category.objects.all(),
    comment = Comment.objects.filter(news=news)
    
    context = {
        "news": news,
        "photo": image,
        'category': catebory_list,
        'comment': comment
    }
    
    return render(request, 'main/news_page.html', context)


def politics_view(request):
    news = News.objects.filter(type_of_category='п')
    image = Photo.objects.filter(news__in=news)
    
    context = {
        "photo": image,
        "news": news
    }
    
    return render(request, 'main/politics.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            messages.error(request, _("Будь ласка, заповніть всі обов'язкові поля."))
            return redirect('register')

        if password1 != password2:
            messages.error(request, _("Паролі не співпадають."))
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, _("Це ім'я користувача вже зайняте."))
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, _("Ця електронна пошта вже використовується."))
            return redirect('register')

        user = User.objects.create_user(
            username=username, 
            password=password1, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
        )
        user.save()
        messages.success(request, _("Ваш обліковий запис успішно створено!"))
        return redirect('login') 

    return render(request, 'main/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, _("Ви успішно увійшли до системи!"))
            return redirect('main')
        else:
            messages.error(request, _("Неправильне ім'я користувача або пароль."))
            return redirect('login')

    return render(request, 'main/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


    