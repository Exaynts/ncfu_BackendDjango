from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', views.HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='category'),
    path('<int:news_id>/', views.ViewNews.as_view(), name='view_news'),
    path('add_news/', views.CreateNews.as_view(), name='add_news'),
    path('<int:news_id>/edit/', views.UpdateNews.as_view(), name='update_news'),
    path('<int:news_id>/delete/', views.DeleteNews.as_view(), name='delete_news'),
    path('my-news/', views.UserNewsListView.as_view(), name='user_news'),
    path('captcha/', include('captcha.urls')),
    path('test/', views.test_pagination, name='test_pagination'),
    path('contact/', views.contact, name='contact'),
    path('', cache_page(60)(views.HomeNews.as_view()), name='home'),
]
