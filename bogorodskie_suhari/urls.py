from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),       # Личный кабинет и аутентификация
    path('', include('shop.urls')),               # Магазин и корзина
    path('info/', include('info.urls')),          # Описание организации и новости
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)