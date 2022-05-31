from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddPostForm
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'app1/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True)



def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app1/about.html', {'page_obj': page_obj, "title": "О сайте", 'menu': menu})


# Добавление статьи
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'app1/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def contact(request):
    return render(request, 'app1/contact.html', {"title": "Контакт", 'menu': menu})


def login(request):
    return HttpResponse('Авторизация')


# Вывод статьи
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'app1/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена. Вам точно нужна эта страница??</h1>')


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'app1/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context
