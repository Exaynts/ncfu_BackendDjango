''' Вход в админку: Логин: admin Пароль: 1'''
''' Вход для пользователя Jammy: Novanov2020'''

from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import News, Category

# Форма для CKEditor (для поля content)
class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title', 'category__title')
    list_filter = ('is_published', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)