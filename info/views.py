from django.shortcuts import render

from shop.models import Product
from .models import OrganizationInfo, News

def organization_info(request):
    info = OrganizationInfo.objects.first()
    return render(request, 'info/organization_info.html', {'info': info})

def news_list(request):
    news = News.objects.order_by('-created_at')[:10]
    return render(request, 'info/news_list.html', {'news': news})

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})