from django.shortcuts import render
from django.http import HttpResponse
from .models import News, Category


def index(request):
    news = News.objects.all()
    news_context = {
        'news': news,
        'title': 'Наш списочек новостей',
    }
    return render(request, template_name='news/index.html', context=news_context)

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, template_name='news/category.html', context={
        'news': news,
        'category': category
    })

def test(request):
    print(request)
    print(dir(request))
    return HttpResponse('It is test page')

def root_page(request):
    return render(request, 'root.html')

