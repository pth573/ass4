from django.urls import path
from .views import create_payment, get_payment, update_payment_status

urlpatterns = [
    path('payments/<int:order_id>/create/', create_payment, name='create_payment'),
    path('payments/<int:order_id>/', get_payment, name='get_payment'),
    path('payments/<int:order_id>/update-status/', update_payment_status, name='update_payment_status'),
]
