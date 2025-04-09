from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    established_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "mobile"

class Screen(models.Model):
    size = models.FloatField()  # Screen size (inches)
    resolution = models.CharField(max_length=50)  # Resolution (Example: "1080x2400")
    refresh_rate = models.IntegerField()  # Refresh rate (Hz)

    def __str__(self):
        return f"{self.size} inch {self.resolution} ({self.refresh_rate}Hz)"

class Battery(models.Model):
    capacity = models.IntegerField()  # Battery capacity (mAh)
    type = models.CharField(max_length=50)  # Battery type (Example: "Li-Ion", "Li-Po")

    def __str__(self):
        return f"{self.type} - {self.capacity}mAh"

from django.db import models

class Camera(models.Model):
    resolution = models.CharField(max_length=50)  # Resolution (Example: "48MP")
    lens_count = models.IntegerField()  # Number of lenses (Example: 3)

    def __str__(self):
        return f"{self.resolution} ({self.lens_count} lenses)"

class Storage(models.Model):
    type = models.CharField(max_length=50)  # Memory type (Example: "UFS 3.1", "eMMC 5.1")
    size = models.IntegerField()  # Size (GB)

    def __str__(self):
        return f"{self.size}GB - {self.type}"

class Mobile(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.SET_NULL, null=True, blank=True)
    battery = models.ForeignKey(Battery, on_delete=models.SET_NULL, null=True, blank=True)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Mobile {self.id} - {self.brand.name}"
