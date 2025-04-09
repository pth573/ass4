from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Shipping
from .serializers import ShippingSerializer
import requests

ORDER_API_URL = "http://127.0.0.1:8000/api/orders/"

@api_view(['POST'])
def create_shipping(request, order_id):
    """Generate shipping information from order"""

    order_response = requests.get(f"{ORDER_API_URL}{order_id}/")

    if order_response.status_code != 200:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    order_data = order_response.json()

    if isinstance(order_data, list) and len(order_data) > 0:
        order_data = order_data[0]

    if not isinstance(order_data, dict) or "customer_id" not in order_data:
        return Response({"error": "Invalid order data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    shipping = Shipping.objects.create(
        order_id=order_id,
        customer_id=order_data["customer_id"],
        address=request.data.get("address"),
    )

    return Response(ShippingSerializer(shipping).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_shipping(request, order_id):
    """Get all shipping information for a specific order"""

    shippings = Shipping.objects.filter(order_id=order_id)

    if not shippings.exists():
        return Response({"error": "No shipping information found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(ShippingSerializer(shippings, many=True).data, status=status.HTTP_200_OK)

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Shipping
from .serializers import ShippingSerializer

ORDER_API_URL = "http://localhost:8000/api/orders/"

@api_view(['PATCH'])
def update_shipping_status(request, order_id):
    """Update shipping status và cập nhật luôn status đơn hàng"""

    shippings = Shipping.objects.filter(order_id=order_id)

    if not shippings.exists():
        return Response({"error": "No shipping information found"}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get("status")

    if new_status not in dict(Shipping.STATUS_CHOICES):
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    # Cập nhật tất cả các shipping
    for shipping in shippings:
        shipping.status = new_status
        shipping.save()

    # Gọi API để cập nhật trạng thái đơn hàng sang "shipped"
    order_data = {}
    try:
        order_response = requests.patch(
            f"{ORDER_API_URL}{order_id}/update-status/",
            json={"status": "shipped"}
        )

        if order_response.status_code == 200:
            order_data = order_response.json()
        else:
            order_data = {"warning": "Failed to update order status"}

    except requests.exceptions.RequestException as e:
        order_data = {"warning": f"Failed to contact order service. {str(e)}"}

    return Response({
        "shippings": ShippingSerializer(shippings, many=True).data,
        "order_info": order_data,
    }, status=status.HTTP_200_OK)

