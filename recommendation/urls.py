from django.urls import path

from .views import recommend_products

urlpatterns = [

path('recommendations/<int:customer_id>/', recommend_products, name='recommend_products'),

]