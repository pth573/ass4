"""
URL configuration for hang_project4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('customer.urls')),
    path('api/', include('vip.urls')),  
    path('api/', include('regular.urls')),
    path('api/', include('book.urls')), 
    path('api/', include('clothes.urls')),  
    path('api/', include('cart.urls')), 
    path('api/', include('product.urls')),  
    path('api/', include('laptop.urls')),  
    path('api/', include('mobile.urls')),  
    path('api/', include('order.urls')),  
    path('api/', include('paying.urls')),  
    path('api/', include('recommendation.urls')),  
    path('api/', include('review.urls')), 
    path('api/', include('review_analysis.urls')),  
    path('api/', include('shipping.urls')), 
]
