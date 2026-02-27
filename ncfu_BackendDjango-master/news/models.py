from django.db import models


class Category(models.Model):
    title = models.CharField(max_length = 150, db_index = True, verbose_name = 'Наименование нашей категории')
    class Meta:
        verbose_name = 'Наша категория'
        verbose_name_plural = 'Наши категории'
        ordering = ['title']
    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length = 150, verbose_name = 'Наименование')
    content = models.TextField(blank = True, verbose_name = 'Ободряющий контент')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата публикации')
    updated_at = models.DateTimeField(auto_now = True, verbose_name = 'Обновлено')
    photo = models.ImageField(upload_to = 'photos/%Y/%m/%d', verbose_name = 'Фоточка', blank=True)
    is_published = models.BooleanField(default = True, verbose_name = 'Опубликировано')
    # Объединяем новости в категорию и защищаем их от удаления и позволяем иметь пустые поля,
    category = models.ForeignKey(Category, on_delete = models.PROTECT, null = True, verbose_name='Кагерогюшка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость' #Наименование в единственном числе
        verbose_name_plural = 'Новости' #Наименование во множественном числе
        ordering = ['-created_at',] #Порядок сортировки. В данном случае от самой новой новости

