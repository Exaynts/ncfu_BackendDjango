from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsModelForm   # импортируем связанную форму


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


def get_categories():
    return Category.objects.all()


def test(request):
    print(request)
    print(dir(request))
    return HttpResponse('It is test page')


def root_page(request):
    return render(request, 'root.html')


def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
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