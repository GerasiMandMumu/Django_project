from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]


def index(request):
    posts = Women.objects.all()

    context = {
        'posts': posts,
        "title": "Главная страница",
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'app1/index.html', context=context)


def about(request):
    return render(request, 'app1/about.html', {"title": "О сайте", 'menu': menu})


def addpage(request):
    return HttpResponse('Добавление статьи')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id = {post_id}')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)

    if len(posts) == 0:
        raise  Http404()

    context = {
        'posts': posts,
        "title": "Рубрики",
        'menu': menu,
        'cat_selected': cat_id,
    }
    return render(request, 'app1/index.html', context=context)