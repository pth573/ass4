from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, PublisherViewSet, GenreViewSet, BookViewSet, update_book

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('books/', include (router.urls)),
    path('books/books/<int:pk>/update/', update_book, name='update-book')
]