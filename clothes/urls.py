from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clothes.views import BrandViewSet, SizeViewSet, MaterialViewSet, ColorViewSet, ClothesViewSet, update_clothes

router = DefaultRouter()

router.register(r'brands', BrandViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'clothes', ClothesViewSet)

urlpatterns = [
    path('clothes/', include(router.urls)),
    path('clothes/clothes/<int:pk>/update/', update_clothes, name='update-clothes'),
]
