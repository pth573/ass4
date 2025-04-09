from django.urls import path
from .views import create_order, get_orders, update_order_status

urlpatterns = [
    path('orders/<int:customer_id>/create/', create_order, name='create_order'),
    path('orders/<int:customer_id>/', get_orders, name='get_orders'),
    path('orders/<int:order_id>/update-status/', update_order_status, name='update_order_status'),
]
