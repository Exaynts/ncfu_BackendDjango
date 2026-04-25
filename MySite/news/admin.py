''' Вход в админку: Логин: admin Пароль: 1'''

from django.contrib import admin
from .models import News, Category

class IdFilter(admin.SimpleListFilter):
    title = 'по ID'
    parameter_name = 'id_filter'

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', "category__title")
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category',)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', "category__title") #Ставим запятую в конце, чтобы указать,
    # что у нас в аргументе стоит кортеж, являющиимя последним аргументом
admin.site.register(News, NewsAdmin)
admin.site.register(Category)

