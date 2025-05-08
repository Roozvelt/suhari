from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('organization_info/', views.organization_info, name='organization_info'),
    path('news/', views.news_list, name='news_list'),
    path('index/', views.index, name='index'),
]