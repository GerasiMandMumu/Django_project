from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddPostForm
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
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            try:
                Women.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    return render(request, 'app1/addpage.html', {"form": form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        "title": post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'app1/post.html', context)


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