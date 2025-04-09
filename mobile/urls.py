from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mobile.views import BrandMobileViewSet, ScreenViewSet, BatteryViewSet, CameraViewSet, StorageViewSet, MobileViewSet, update_mobile

router = DefaultRouter()

router.register(r'brands', BrandMobileViewSet)
router.register(r'screens', ScreenViewSet)  # Sửa lỗi dấu phẩy
router.register(r'batteries', BatteryViewSet)
router.register(r'cameras', CameraViewSet)
router.register(r'storages', StorageViewSet)
router.register(r'mobiles', MobileViewSet)

urlpatterns = [
    path('mobiles/', include(router.urls)),  
    path('mobiles/mobiles/<int:pk>/update/', update_mobile, name='update-mobile'),
]
