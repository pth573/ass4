from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('laptop', 'Laptop'),
        ('book', 'Book'),
        ('mobile', 'Mobile'),
        ('clothes', 'Clothes'),
    )

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.category})"
