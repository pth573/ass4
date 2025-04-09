from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now

class Shipping(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]

    order_id = models.IntegerField()
    customer_id = models.IntegerField()
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipped_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"Shipping for Order {self.order_id} - {self.status}"
