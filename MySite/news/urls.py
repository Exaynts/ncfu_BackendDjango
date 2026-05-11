from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeNews.as_view(), name='home'),
    path('test/', views.test),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='category'),
    path('<int:news_id>/', views.ViewNews.as_view(), name='view_news'),
    path('add_news/', views.CreateNews.as_view(), name='add_news'),
    path('<int:news_id>/edit/', views.UpdateNews.as_view(), name='update_news'),
    path('<int:news_id>/delete/', views.DeleteNews.as_view(), name='delete_news'),
]
