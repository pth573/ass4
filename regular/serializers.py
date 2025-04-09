import requests
from rest_framework import serializers
from .models import RegularCustomer

class RegularCustomerSerializer(serializers.ModelSerializer):
    customer_info = serializers.SerializerMethodField()

    class Meta:
        model = RegularCustomer
        fields = ['id', 'customer_id', 'discount_rate', 'customer_info']

    def get_customer_info(self, obj):
        url = f"http://127.0.0.1:8000/api/customers/{obj.customer_id}/"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
