from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

# Sử dụng router để tự động tạo URL CRUD cho Customer
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
