from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test/', views.test),
    path('category/<int:category_id>/', views.get_category, name='category'),
    path('news/<int:news_id>/', views.view_news, name='view_news'),
]
