from django import forms
from django.core.exceptions import ValidationError
from .models import News
import os
from better_profanity import profanity
from django.conf import settings

# Загрузка стандартного словаря
profanity.load_censor_words()

# Добавление русских слов
def load_russian_badwords():
    file_path = os.path.join(settings.BASE_DIR, 'news/vocabularies', 'bad_russian_words.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        if words:
            profanity.add_censor_words(words)  # добавление к уже загруженному списку
    except FileNotFoundError:
        pass

load_russian_badwords()

class NewsModelForm(forms.ModelForm):
    author = forms.CharField(
        label='Автор',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'is_published', 'category', 'author']
        labels = {
            'title': 'Название',
            'content': 'Содержание',
            'photo': 'Изображение',
            'is_published': 'Опубликовать?',
            'category': 'Категория',
            'author': 'Автор',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['author'].required = False
        profanity.load_censor_words()
        # Добавление bad_russian_words.txt слов из файла  к стандартному словарю
        profanity.load_censor_words_from_file('news/vocabularies/bad_russian_words.txt')

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError('Название не может быть пустым!')
        if len(title) < 5:
            raise ValidationError('Название новости слишком короткое. Длина должна быть не менее пяти символов!')
        if len(title) > 100:
            raise ValidationError('Название новости слишком длинное. Длина должна быть не более ста символов!')
        if profanity.contains_profanity(title):
            raise ValidationError('Всмысле?! Не выражайтесь!')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if profanity.contains_profanity(content):
            raise ValidationError('Не выражайтесь в описании новости!')
        return content