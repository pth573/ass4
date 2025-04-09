from django.urls import path

from .views import (
    get_all_reviews,
    get_reviews_by_customer,
    get_reviews_by_product,
    add_review,
    get_full_reviews,
    analyze_customer_reviews,
    get_review_by_id,
    analyze_review_by_id,
)

urlpatterns = [
    path('reviews/', get_all_reviews, name='get_all_reviews'),
    path('reviews/<int:review_id>/', get_review_by_id, name='get_review_by_id'),
    path('reviews/customer/<int:customer_id>/', get_reviews_by_customer, name='get_reviews_by_customer'),
    path('reviews/products/<str:category>/<int:product_id>/', get_reviews_by_product, name='get_reviews_by_product'),
    path('reviews/add/', add_review, name='add_review'),
    path('reviews/full/', get_full_reviews, name='get_full_reviews'),
    path('reviews/customer/<int:customer_id>/analyze/', analyze_customer_reviews, name='analyze_customer_reviews'),
    path('reviews/<int:review_id>/analyze/', analyze_review_by_id, name='analyze_review_by_id'),
    # path('reviews/product/<str:category>/<int:product_id>/', get_reviews_by_product, name='get_reviews_by_product'),

]
