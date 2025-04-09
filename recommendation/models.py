from django.db import models

# Create your models here.
from django.db import models

class Recommendation(models.Model):
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    category = models.CharField(max_length=50)
    score = models.FloatField()

    def __str__(self):
        return f"Recommendation for Customer {self.customer_id} on Product {self.product_id} - Category: {self.category} with Score {self.score}"
