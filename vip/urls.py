from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import VIPCustomerViewSet

router = DefaultRouter()
router.register(r'vip-customers', VIPCustomerViewSet)

urlpatterns = [
    path('', include (router.urls)),
]