from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import News, Category
from .forms import NewsModelForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .utils import MyMixin
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# Классовые представления

class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = True
    paginate_by = 6
    mixin_prop = 'Hello, Jam!'

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['upper_title'] = self.get_upper(context['title'])
        context['mixin_prop'] = self.get_prop()
        return context


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = True
    paginate_by = 6

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return News.objects.filter(category_id=category_id, is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context['category'] = category
        context['upper_category_title'] = self.get_upper(category.title)
        return context


class ViewNews(MyMixin, DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'
    pk_url_kwarg = 'news_id'

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upper_title'] = self.get_upper(self.object.title)
        return context


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsModelForm
    template_name = 'news/create_news.html'
    login_url = '/login/'

    def get_initial(self):
        return {'author': self.request.user.username}

    def form_valid(self, form):
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


class UserNewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = True
    paginate_by = 6

    def get_queryset(self):
        return News.objects.filter(author=self.request.user.username, is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои новости'
        context['upper_title'] = self.get_upper(context['title'])
        return context


# Функциональные представления

def test_pagination(request):
    objects_list = [f"Элемент {i}" for i in range(1, 101)]   # 100 элементов
    paginator = Paginator(objects_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/test.html', {'page_obj': page_obj})


def root_page(request):
    return render(request, 'root.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                subject=f'Сообщение от {name}',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['admin@example.com'],
                fail_silently=True,
            )
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {'form': form})