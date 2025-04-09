from django.db import models

# Create your models here.
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    founded_year = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

class Storage(models.Model):
    type = models.CharField(max_length=50, unique=True)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    speed = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.capacity}"

class Screen(models.Model):
    size = models.CharField(max_length=50, unique=True)
    resolution = models.CharField(max_length=100, null=True, blank=True)
    refresh_rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.size} - {self.resolution}"

from django.db import models

class GPU(models.Model):
    name = models.CharField(max_length=100, unique=True)
    vram = models.CharField(max_length=50, null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.vram}"

class Laptop(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="laptops")
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, blank=True)
    screen = models.ForeignKey(Screen, on_delete=models.SET_NULL, null=True, blank=True)
    gpu = models.ForeignKey(GPU, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
