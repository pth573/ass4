from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    order_id = models.IntegerField()
    customer_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"Payment for Order {self.order_id} - {self.status}"
