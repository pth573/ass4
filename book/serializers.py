from rest_framework import serializers
from .models import Author, Publisher, Genre, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    publisher = PublisherSerializer()
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        publisher_data = validated_data.pop('publisher', None)
        genre_data = validated_data.pop('genre', None)

        author = None
        if author_data:
            author = Author.objects.filter(**author_data).first()
            if not author:
                author = Author.objects.create(**author_data)

        publisher = None
        if publisher_data:
            publisher = Publisher.objects.filter(**publisher_data).first()
            if not publisher:
                publisher = Publisher.objects.create(**publisher_data)

        genre = None
        if genre_data:
            genre = Genre.objects.filter(**genre_data).first()
            if not genre:
                genre = Genre.objects.create(**genre_data)

        book = Book.objects.create(author=author, publisher=publisher, genre=genre, **validated_data)
        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        publisher_data = validated_data.pop('publisher', None)
        genre_data = validated_data.pop('genre', None)

        if author_data:
            author = Author.objects.filter(**author_data).first()
            if not author:
                author = Author.objects.create(**author_data)
            instance.author = author

        if publisher_data:
            publisher = Publisher.objects.filter(**publisher_data).first()
            if not publisher:
                publisher = Publisher.objects.create(**publisher_data)
            instance.publisher = publisher

        if genre_data:
            genre = Genre.objects.filter(**genre_data).first()
            if not genre:
                genre = Genre.objects.create(**genre_data)
            instance.genre = genre

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
