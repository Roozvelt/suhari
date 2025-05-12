from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),       # Личный кабинет и аутентификация
    path('shop/', include('shop.urls')),               # Магазин и корзина
    path('info/', include('info.urls')),          # Описание организации и новости
    path('', RedirectView.as_view(url='/info/index'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)