from rest_framework import serializers
from .models import Product

# Nếu muốn serialize từ model (dữ liệu tạm nếu cần)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'category']

# Serializer chỉ gồm 3 trường cơ bản (không liên quan model)
class BasicProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
