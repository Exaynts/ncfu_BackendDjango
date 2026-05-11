from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsModelForm

def index(request):
    news = News.featured.get_visible_for_user(request.user)
    news_context = {
        'news': news,
        'title': 'Наш списочек новостей',
    }
    return render(request, template_name='news/index.html', context=news_context)

def get_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    news = News.featured.get_visible_for_user(request.user).filter(category_id=category_id)
    return render(request, template_name='news/category.html', context={
        'news': news,
        'category': category,
    })

def get_categories():
    return Category.objects.all()

def view_news(request, news_id):
    news_item = get_object_or_404(News.featured.get_visible_for_user(request.user), pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})

def add_news(request):
    if request.method == 'POST':
        form = NewsModelForm(request.POST, request.FILES)
        if form.is_valid():
            news_item = form.save()
            return redirect(news_item.get_absolute_url())
    else:
        form = NewsModelForm()
    return render(request, 'news/add_news.html', {'form': form})

def test(request):
    return HttpResponse('It is test page')

def root_page(request):
    return render(request, 'root.html')