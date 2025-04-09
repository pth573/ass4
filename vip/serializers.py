import requests
from rest_framework import serializers
from .models import VIPCustomer

class VIPCustomerSerializer(serializers.ModelSerializer):
    customer_info = serializers.SerializerMethodField()

    class Meta:
        model = VIPCustomer
        fields = ['id', 'customer_id', 'membership_level', 'customer_info']

    def get_customer_info(self, obj):
        url = f"http://127.0.0.1:8000/api/customers/{obj.customer_id}/"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
