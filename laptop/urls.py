from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, StorageViewSet, ScreenViewSet, GPUViewSet, LaptopViewSet, update_laptop

router = DefaultRouter()

router.register(r'brands', BrandViewSet)
router.register(r'storages', StorageViewSet)
router.register(r'screens', ScreenViewSet)
router.register(r'gpus', GPUViewSet)
router.register(r'laptops', LaptopViewSet)

urlpatterns = [
    path('laptops/', include(router.urls)),
    path('laptops/laptops/<int:pk>/update/', update_laptop, name='update-laptop'),
]
