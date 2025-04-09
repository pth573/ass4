from django.urls import path
from .views import create_shipping, get_shipping, update_shipping_status

urlpatterns = [
    path('shippings/<int:order_id>/create/', create_shipping, name='create_shipping'),
    path('shippings/<int:order_id>/', get_shipping, name='get_shipping'),
    path('shippings/<int:order_id>/update-status/', update_shipping_status, name='update_shipping_status'),
]
