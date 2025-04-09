from django.urls import path
from .views import (
    get_all_products,
    get_all_basic_products,
    get_products_by_category,
    get_product_detail,
    update_product_quantity,
)

from .views import get_products_by_category_plural

urlpatterns = [
    path('products/', get_all_products),
    path('products/basic/', get_all_basic_products),
    path('products/<str:category_plural>', get_products_by_category_plural),
    path('products/<str:category>/', get_products_by_category),
    path('products/<str:category>/<int:product_id>/', get_product_detail),
    path('products/<str:category>/<int:product_id>/update/', update_product_quantity),
]
