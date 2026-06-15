from django import template
from news.models import Category
from django.db.models import Count
from django.core.cache import cache

register = template.Library()

@register.simple_tag(name='get_categories')
def get_categories(name='get_list_categories'):
    return Category.objects.all()

@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Последние', arg2='новости'):
    categories = cache.get('categories')
    if categories is None:
        categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
        cache.set('categories', categories, 60)
    return {'categories': categories, "arg1": arg1, "arg2": arg2}