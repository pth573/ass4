from django.urls import path
from .views import RegisterAPIView, CustomerListCreateView, CustomerDetailView

from .views import LoginAPIView

urlpatterns = [
    path('customers/register/', RegisterAPIView.as_view(), name='customer-register'),
    path('customers/login/', LoginAPIView.as_view(), name='customer-login'),  
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
]
