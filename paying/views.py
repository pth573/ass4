from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
import requests

ORDER_API_URL = "http://127.0.0.1:8000/api/orders/"

@api_view(['POST'])
def create_payment(request, order_id):
    """Create payment for order"""
    order_response = requests.get(f"{ORDER_API_URL}{order_id}/")

    if order_response.status_code != 200:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    order_data = order_response.json()

    if isinstance(order_data, list) and len(order_data) > 0:
        order_data = order_data[0]

    if not isinstance(order_data, dict):
        return Response({"error": "Invalid order data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    payment = Payment.objects.create(
        order_id=order_id,
        customer_id=order_data["customer_id"],
        amount=order_data["total_price"]
    )

    return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_payment(request, order_id):
    """Get all payment information for a given order_id"""
    payments = Payment.objects.filter(order_id=order_id)

    if not payments.exists():
        return Response({"error": "No payment information found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(PaymentSerializer(payments, many=True).data)



ORDER_API_URL = "http://localhost:8000/api/orders/"  
from django.db.models import Count

@api_view(['PATCH'])
def update_payment_status(request, order_id):
    """Update payment status và cập nhật luôn status đơn hàng"""
    payments = Payment.objects.filter(order_id=order_id)

    if not payments.exists():
        return Response({"error": "No payment information found"}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get("status")

    if new_status not in dict(Payment.STATUS_CHOICES):
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    # Cập nhật tất cả các payment
    for payment in payments:
        payment.status = new_status
        payment.save()

    # Gọi API để cập nhật trạng thái đơn hàng
    order_data = {}
    try:
        order_response = requests.patch(
            f"{ORDER_API_URL}{order_id}/update-status/",
            json={"status": "paid"}
        )

        if order_response.status_code == 200:
            order_data = order_response.json()
        else:
            order_data = {"warning": "Failed to update order status"}

    except requests.exceptions.RequestException as e:
        order_data = {"warning": f"Failed to contact order service. {str(e)}"}


    return Response({
        "payments": PaymentSerializer(payments, many=True).data,
        "order_info": order_data,
    }, status=status.HTTP_200_OK)
