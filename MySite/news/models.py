from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
import re


class NewsManager(models.Manager):
    """Кастомный менеджер для получения новостей с учётом прав пользователя"""

    def get_visible_for_user(self, user):
        qs = super().get_queryset()
        if not user.is_staff:
            qs = qs.filter(is_published=True)
        return qs


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование нашей категории')

    class Meta:
        verbose_name = 'Наша категория'
        verbose_name_plural = 'Наши категории'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Ободряющий контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фоточка', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name='Категория')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='Автор')
    views = models.IntegerField(default=0)


    objects = models.Manager()
    featured = NewsManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'news_id': self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
