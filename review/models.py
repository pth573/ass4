from django.db import models

# Create your models here.
from django.db import models

class Review(models.Model):
    category = models.CharField(max_length=50, default="mobile")
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review for Product {self.product_id} by Customer {self.customer_id}"
