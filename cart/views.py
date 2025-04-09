from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from .serializers import CartItemSerializer
import requests

API_ENDPOINTS = {
    "mobiles": "http://127.0.0.1:8000/api/mobiles/mobiles/",
    "laptops": "http://127.0.0.1:8000/api/laptops/laptops/",
    "clothes": "http://127.0.0.1:8000/api/clothes/clothes/",
    "books": "http://127.0.0.1:8000/api/books/books/",
}

@api_view(['POST'])
def add_to_cart(request):
    data = request.data
    customer_id = data.get("customer_id")
    category = data.get("category")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not customer_id or not category or not product_id or quantity <= 0:
        return Response({"error": "Invalid information"}, status=status.HTTP_400_BAD_REQUEST)

    if category not in API_ENDPOINTS:
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)

    api_url = f"{API_ENDPOINTS[category]}{product_id}/"
    response = requests.get(api_url)

    if response.status_code != 200:
        return Response({"error": "No product found"}, status=status.HTTP_400_BAD_REQUEST)

    product_data = response.json()
    stock_quantity = product_data.get("quantity", 0)

    if stock_quantity < quantity:
        return Response({"error": "Insufficient product quantity"}, status=status.HTTP_400_BAD_REQUEST)

    cart_item, created = CartItem.objects.get_or_create(
        customer_id=customer_id,
        category=category,
        product_id=product_id,
        defaults={
            "name": product_data.get("name", "Unknown"),
            "price": product_data.get("price", 0),
            "quantity": quantity
        }
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    update_stock_url = f"http://127.0.0.1:8000/api/products/{category}/{product_id}/update/"
    update_data = {"quantity": stock_quantity - quantity}
    requests.put(update_stock_url, json=update_data)

    return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_cart(request, customer_id):
    cart_items = CartItem.objects.filter(customer_id=customer_id)
    customer_url = f"http://127.0.0.1:8000/api/customers/{customer_id}/"
    customer_response = requests.get(customer_url)

    if customer_response.status_code != 200:
        return Response({"error": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)

    customer_data = customer_response.json()
    cart_data = []

    for item in cart_items:
        api_url = f"{API_ENDPOINTS[item.category]}{item.product_id}/"
        response = requests.get(api_url)

        product_data = response.json() if response.status_code == 200 else {
            "id": item.product_id,
            "name": "No product found",
            "price": item.price,
        }

        cart_data.append({
            "id": item.id,
            "category": item.category,
            "product_id": item.product_id,
            "name": product_data.get("name", "Unknown"),
            "price": product_data.get("price", item.price),
            "quantity": item.quantity
        })

    return Response({"customer": customer_data, "cart": cart_data})

@api_view(['DELETE'])
def remove_from_cart(request, customer_id, cart_item_id):
    try:
        item = CartItem.objects.get(id=cart_item_id, customer_id=customer_id)
        item.delete()
        return Response({"message": "Product removed from cart"}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)