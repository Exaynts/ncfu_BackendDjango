from django import forms
import re
from django.core.exceptions import ValidationError
from .models import Category, News

def validate_title_not_start_with_digit(value):
    if value and value[0].isdigit():
        raise ValidationError('Название не может начинаться с цифры')

def validate_author_name_length(value):
    if value and len(value.strip()) < 3:
        raise ValidationError('Имя автора слишком короткое. Длина имени должна быть больше двух букв!')
    elif value and len(value.strip()) > 100:
        raise ValidationError('Имя автора слишком длинное. Длина имени должна быть не более ста букв!')
    elif value and 'Неизвестен' in value:
        raise ValidationError('Пожалуйста, не включайте в название автора слово "Неизвестен"!')

class NewsModelForm(forms.ModelForm):
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
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['title'].validators.append(validate_title_not_start_with_digit)
        self.fields['author'].validators.append(validate_author_name_length)
        self.fields['author'].required = False

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры!')
        return title