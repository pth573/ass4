from django.db import models

# Create your models here.
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    established_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    size = models.CharField(max_length=10, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.size

class Material(models.Model):
    type = models.CharField(max_length=100, unique=True)
    durability = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.type

from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, unique=True)  # Mã màu HEX
    category = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.hex_code})"

class Clothes(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Clothes {self.id} - {self.brand.name} - {self.price} VND {self.quantity} pcs"
