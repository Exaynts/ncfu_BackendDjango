from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from news.views import root_page
from news.views import *
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('', include('users.urls')),
    path('', root_page, name='root_page'),
    path("__reload__/", include("django_browser_reload.urls")),
] + debug_toolbar_urls() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

