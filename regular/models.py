from django.db import models

# Create your models here.
from django.db import models
import requests

class RegularCustomer(models.Model):
    customer_id = models.IntegerField()
    discount_rate = models.FloatField(default=0.05)

    def get_customer(self):
        response = requests.get(f"http://127.0.0.1:8000/api/customers/{self.customer_id}/")
        return response.json() if response.status_code == 200 else None

    def __str__(self):
        customer = self.get_customer()
        return f"Regular {customer.get('full_name', {}).get('first_name', '')} {customer.get('full_name', {}).get('last_name', '')}" if customer else ""
