from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response  # đúng cái này
from rest_framework import status
from rest_framework import viewsets
from .models import Author, Publisher, Genre, Book
from .serializers import AuthorSerializer, PublisherSerializer, GenreSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['PUT'])
def update_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get("quantity")
    if quantity is None:
        return Response({"error": "Missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

    book.quantity = quantity
    book.save()

    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)