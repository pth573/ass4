from django.db import models

# Create your models here.
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    founded_year = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    quantity = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.author.name if self.author else 'Unknown'} {self.language} {self.price} VND {self.quantity} pcs"
