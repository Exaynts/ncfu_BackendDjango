from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News, Category
from .forms import NewsModelForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Классовые представления
class HomeNews(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = True

    def get_queryset(self):
        # Показываем только опубликованные новости
        return News.objects.filter(is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class NewsByCategory(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = True

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return News.objects.filter(category_id=category_id, is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_object_or_404(Category, pk=category_id)
        return context


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'
    pk_url_kwarg = 'news_id' # позволяет использовать параметр news_id из URL

    def get_queryset(self):
        # Доступ к детальной странице имеют только опубликованные новости
        return News.objects.filter(is_published=True)


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsModelForm
    template_name = 'news/create_news.html'

    def get_initial(self):
        # Предзаполняем поле author именем текущего пользователя
        return {'author': self.request.user.username}

    def form_valid(self, form):
        # Убеждаемся, что автор не может быть изменён через POST
        form.instance.author = self.request.user.username
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class UpdateNews(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsModelForm
    template_name = 'news/update_news.html'
    pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'

    def get_initial(self):
        return {'author': self.request.user.username}

    def form_valid(self, form):
        form.instance.author = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        # Право на редактирование есть только у автора новости или суперпользователя
        news = self.get_object()
        return self.request.user.is_superuser or news.author == self.request.user.username

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteNews(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    pk_url_kwarg = 'news_id'
    success_url = reverse_lazy('home')
    template_name = 'news/delete_news.html'

    def test_func(self):
        news = self.get_object()
        return self.request.user.is_superuser or news.author == self.request.user.username

# Функциональные представления
def test():
    return HttpResponse('It is test page')


def root_page(request):
    return render(request, 'root.html')