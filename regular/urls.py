from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegularCustomerViewSet

router = DefaultRouter()
router.register(r'regular-customers', RegularCustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
