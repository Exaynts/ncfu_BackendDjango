from django import template
from news.models import Category

register = template.Library()

 # Тег для получения списка категорий
register=template.Library()
@register.simple_tag(name='get_categories')
def get_categories(name='get_list_categories'):
    return Category.objects.all()

# Тег включения для отображения списка категорий с рендерингом шаблона
@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Последние', arg2='новости'):
    categories = Category.objects.all()
    return {'categories': categories, "arg1": arg1, "arg2": arg2}