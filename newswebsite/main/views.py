from django.http import HttpRequest
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import os

from dotenv import load_dotenv

load_dotenv()


def main_view(request): 
    
    adds = Advertising.objects.all()
    
    news_list = News.objects.prefetch_related('photo').all()
    paginate = Paginator(news_list, 5)
    page = request.GET.get('page')
    
    try:
        posts = paginate.page(page)
    except PageNotAnInteger:
        posts = paginate.page(1)
    except EmptyPage:
        posts = paginate.page(paginate.num_pages)
    
    trending_news = TrendingNews.objects.select_related('news').order_by('-news__date_of_publish')[:5]

    
    url = os.getenv('url')
    response = requests.get(url)
    
    
    try:
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
        
    except requests.exceptions.RequestException as e:
        return render(request, 'main/index.html', {'error': f'Помилка запиту: {e}'})
    
    context = {
        "news": news_list,
        'user': request.user,
        'trend': trending_news,
        'posts': posts,
        
        'units': units,
        'tanks': tanks,
        'arm_veh': armoured_vehicles,
        'artillery': artillery,
        'mlrs': mlrs,
        'planes': planes,
        'helicopters': helicopters,
        'fuel_tanks': fuel_tanks,
        'warships': warships, 
        
    }
    
    return render(request, 'main/index.html', context)



def news_template(request, news_id):
    news = get_object_or_404(News, id=news_id)
    image = Photo.objects.filter(news=news)
    comment = Comment.objects.filter(news=news)
    
    
    trending_news = TrendingNews.objects.select_related('news').order_by('-news__date_of_publish')[:5]
    
    url = os.getenv('url')
    response = requests.get(url)
    
    
    try:
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
        
    except requests.exceptions.RequestException as e:
        return render(request, 'main/news_page.html', {'error': f'Помилка запиту: {e}'})
    
    context = {
        "news": news,
        "photo": image,

        'text_comm': comment,
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
    
    
    
    return render(request, 'main/news_page.html', context)


def politics_view(request):
    trending_news = TrendingNews.objects.select_related('news').order_by('-news__date_of_publish')[:5]
    news = News.objects.prefetch_related('photo').filter(type_of_category='п')
    
    paginate = Paginator(news, 5)
    page = request.GET.get('page')
    
    try:
        posts = paginate.page(page)
    except PageNotAnInteger:
        posts = paginate.page(1)
    except EmptyPage:
        posts = paginate.page(paginate.num_pages)
    
    url = os.getenv('url')
    response = requests.get(url)
    
    
    try:
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
        
    except requests.exceptions.RequestException as e:
        return render(request, 'main/politics.html', {'error': f'Помилка запиту: {e}'})
    
    context = {
        "news": news,
        'posts': posts,
        
        'units': units,
        'tanks': tanks,
        'arm_veh': armoured_vehicles,
        'artillery': artillery,
        'mlrs': mlrs,
        'planes': planes,
        'helicopters': helicopters,
        'fuel_tanks': fuel_tanks,
        'warships': warships,
        'trend': trending_news
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


@login_required
def add_comment(request, news_id):

    news = get_object_or_404(News, id=news_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(user=request.user, news=news, comment=comment_text)
            
    
    return redirect('news_template', news_id=news.id)


def currency_view(request):
    news = News.objects.prefetch_related('photo').filter(type_of_category='в')
    token = os.getenv('TOKEN')
    url = os.getenv('url_mono')
    trending_news = TrendingNews.objects.select_related('news').order_by('-news__date_of_publish')[:5]
    
    dollar = None
    euro = None
    
    paginate = Paginator(news, 5)
    page = request.GET.get('page')
    
    try:
        posts = paginate.page(page)
    except PageNotAnInteger:
        posts = paginate.page(1)
    except EmptyPage:
        posts = paginate.page(paginate.num_pages)
    
    try:
        response = requests.get(url)
        
        data_json = response.json()
    
        if response.status_code == 200:
            data = data_json
            dollar = data[0]['rateBuy'], data[0]['rateSell']
            euro = data[1]['rateBuy'], data[1]['rateSell']

    except requests.exceptions.RequestException as e:
        return render(request, 'main/currency.html', {'error': f'Помилка запиту: {e}'})
    except ValueError:
        return render(request, 'main/currency.html', {'error': 'Помилка обробки JSON-відповіді!'})
    
    url = os.getenv('url')
    response = requests.get(url)
    
    
    try:
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
        
    except requests.exceptions.RequestException as e:
        return render(request, 'main/currency.html', {'error': f'Помилка запиту: {e}'})
    
    context = {
        'dollar_view': dollar,
        'euro_view': euro,
        'news': news,
        'posts': posts,
        
        'units': units,
        'tanks': tanks,
        'arm_veh': armoured_vehicles,
        'artillery': artillery,
        'mlrs': mlrs,
        'planes': planes,
        'helicopters': helicopters,
        'fuel_tanks': fuel_tanks,
        'warships': warships,
        'trend': trending_news
    }
    
    return render(request, 'main/currency.html', context)


def tech_view(request):
    news = News.objects.prefetch_related('photo').filter(type_of_category='н')
    trending_news = TrendingNews.objects.select_related('news').order_by('-news__date_of_publish')[:5]
    
    paginate = Paginator(news, 5)
    page = request.GET.get('page')
    
    try:
        posts = paginate.page(page)
    except PageNotAnInteger:
        posts = paginate.page(1)
    except EmptyPage:
        posts = paginate.page(paginate.num_pages)
    
    try:
        url = os.getenv('url')
        response = requests.get(url)
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
    
    except requests.exceptions.RequestException as e:
        return render(request, 'main/tech.html', {'error': f'Помилка запиту: {e}'})
        
    
    context = {
        'news': news,
        'posts': posts,
        
        'units': units,
        'tanks': tanks,
        'arm_veh': armoured_vehicles,
        'artillery': artillery,
        'mlrs': mlrs,
        'planes': planes,
        'helicopters': helicopters,
        'fuel_tanks': fuel_tanks,
        'warships': warships,
        'trend': trending_news
    }
    
    return render(request, 'main/tech.html', context)


def culture_view(request):
    news = News.objects.prefetch_related('photo').filter(type_of_category='к')
    trending_news = TrendingNews.objects.select_related('news').order_by('-news__date_of_publish')[:5]
    
    paginate = Paginator(news, 5)
    page = request.GET.get('page')
    
    try:
        posts = paginate.page(page)
    except PageNotAnInteger:
        posts = paginate.page(1)
    except EmptyPage:
        posts = paginate.page(paginate.num_pages)
    
    url = os.getenv('url')
    response = requests.get(url)
    
    
    try:
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
    
    except requests.exceptions.RequestException as e:
        return render(request, 'main/culture.html', {'error': f'Помилка запиту: {e}'})
        

    
    context = {
        'news': news,
        'posts': posts,
        
        'units': units,
        'tanks': tanks,
        'arm_veh': armoured_vehicles,
        'artillery': artillery,
        'mlrs': mlrs,
        'planes': planes,
        'helicopters': helicopters,
        'fuel_tanks': fuel_tanks,
        'warships': warships,
        'trend': trending_news
    }
    
    return render(request, 'main/culture.html', context)