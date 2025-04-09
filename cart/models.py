from django.db import models

# Create your models here.
from django.db import models

class CartItem(models.Model):
    CATEGORY_CHOICES = [
        ('mobiles', 'Mobile'),
        ('laptops', 'Laptop'),
        ('clothes', 'Clothes'),
        ('books', 'Book'),
    ]

    customer_id = models.IntegerField(default=1)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    product_id = models.IntegerField()
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):  # Sửa lỗi `def_str_` thành `__str__`
        return f"{self.name} - {self.quantity} (Customer {self.customer_id})"
