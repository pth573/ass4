from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart

urlpatterns = [
    path('carts/add/', add_to_cart, name='add_to_cart'),
    path('carts/<int:customer_id>/', view_cart, name='view_cart'),
    path('carts/<int:customer_id>/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
]
