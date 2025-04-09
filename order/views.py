from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer
import requests
import logging

logger = logging.getLogger(__name__)

CART_API_URL = "http://127.0.0.1:8000/api/carts/"

@api_view(['POST'])
def create_order(request, customer_id):
    """Create order from customer's shopping cart"""

    cart_url = f"{CART_API_URL}{customer_id}/"
    cart_response = requests.get(cart_url)

    if cart_response.status_code != 200:
        return Response({"error": "Could not get cart data"}, status=status.HTTP_400_BAD_REQUEST)

    cart_data = cart_response.json()
    cart_items = cart_data.get("cart", [])

    if not cart_items:
        return Response({"error": "Giỏ hàng trống"}, status=status.HTTP_400_BAD_REQUEST)

    total_price = sum(float(item["price"]) * item["quantity"] for item in cart_items)

    order = Order.objects.create(
        customer_id=customer_id,
        total_price=total_price
    )

    order_items = []
    for item in cart_items:
        name = item.get("name")
        if not name:
            logger.warning("Item %s is missing 'name'. Using default 'Unknown'.", item)
            name = "Unknown"  # Đảm bảo có tên mặc định
        
        order_items.append(OrderItem(
            order=order,
            category=item["category"],
            product_id=item["product_id"],
            name=name,  # Đảm bảo giá trị name không trống
            price=item["price"],
            quantity=item["quantity"]
        ))

    OrderItem.objects.bulk_create(order_items)

    for item in cart_items:
        remove_url = f"{CART_API_URL}{customer_id}/remove/{item['id']}/"
        requests.delete(remove_url)

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_orders(request, customer_id):
    """Get customer order list"""

    orders = Order.objects.filter(customer_id=customer_id)
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['PATCH'])
def update_order_status(request, order_id):
    """Update order status"""

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get("status")
    
    if new_status not in dict(Order.STATUS_CHOICES):
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()

    return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
