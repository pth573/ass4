from django.db import models

from django.db import models
import requests

class VIPCustomer(models.Model):
    customer_id = models.IntegerField()
    membership_level = models.CharField(max_length=50, default="Gold")

    def get_customer(self):
        """
        Lấy thông tin khách hàng từ API dựa trên customer_id.
        """
        response = requests.get(f"http://127.0.0.1:8000/api/customers/{self.customer_id}/")
        return response.json() if response.status_code == 200 else None

    def __str__(self):
        """
        Trả về chuỗi mô tả VIP customer với tên đầy đủ của khách hàng.
        """
        customer = self.get_customer()
        if customer:
            first_name = customer.get('full_name', {}).get('first_name', '')
            last_name = customer.get('full_name', {}).get('last_name', '')
            return f"VIP {first_name} {last_name}"
        return "VIP Customer"
