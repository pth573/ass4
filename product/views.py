from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, BasicProductSerializer
import requests

SERVICE_URLS = {
    "laptops": "http://127.0.0.1:8000/api/laptops/laptops/",
    "books": "http://127.0.0.1:8000/api/books/books/",
    "mobiles": "http://127.0.0.1:8000/api/mobiles/mobiles/",
    "clothes": "http://127.0.0.1:8000/api/clothes/clothes/",
}

@api_view(['GET'])
def get_all_products(request):
    """Lấy tất cả sản phẩm từ tất cả service"""
    result = {}
    for category, base_url in SERVICE_URLS.items():
        try:
            response = requests.get(base_url)
            if response.status_code == 200:
                result[category] = response.json()
            else:
                result[category] = f"Failed to fetch {category}"
        except Exception as e:
            result[category] = f"Error: {str(e)}"
    return Response(result)

@api_view(['GET'])
def get_all_basic_products(request):
    """Trả về danh sách tất cả sản phẩm với 3 trường: name, price, quantity"""
    all_products = []
    for base_url in SERVICE_URLS.values():
        try:
            response = requests.get(base_url)
            if response.status_code == 200:
                for item in response.json():
                    # Chỉ lấy 3 trường cơ bản
                    filtered = {
                        'name': item.get('name'),
                        'price': item.get('price'),
                        'quantity': item.get('quantity')
                    }
                    all_products.append(filtered)
        except Exception as e:
            continue  # Bỏ qua lỗi nếu 1 service không hoạt động
    serializer = BasicProductSerializer(all_products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_products_by_category(request, category):
    base_url = SERVICE_URLS.get(category)
    if not base_url:
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)
    response = requests.get(base_url)
    if response.status_code == 200:
        return Response(response.json())
    return Response({"error": "Service error"}, status=response.status_code)

@api_view(['GET'])
def get_product_detail(request, category, product_id):
    base_url = SERVICE_URLS.get(category)
    if not base_url:
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)
    url = f"{base_url}{product_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return Response(response.json())
    return Response({"error": "Product not found"}, status=response.status_code)

# @api_view(['PUT'])
# def update_product_quantity(request, category, product_id):
#     base_url = SERVICE_URLS.get(category)
#     if not base_url:
#         return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)
    
#     quantity = request.data.get("quantity")
#     if quantity is None:
#         return Response({"error": "Missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

#     url = f"{base_url}{product_id}/update/"
#     try:
#         response = requests.put(url, json={"quantity": quantity})
#         return Response(response.json(), status=response.status_code)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_product_quantity(request, category, product_id):
    base_url = SERVICE_URLS.get(category)
    if not base_url:
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)
    
    quantity = request.data.get("quantity")
    if quantity is None:
        return Response({"error": "Missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

    url = f"{base_url}{product_id}/update/"

    try:
        response = requests.put(url, json={"quantity": quantity})
        try:
            data = response.json()  # cố gắng parse JSON
        except ValueError:
            return Response({
                "error": "Backend không trả về JSON hợp lệ",
                "status_code": response.status_code,
                "raw_response": response.text  # cho biết backend trả về gì
            }, status=response.status_code)
        
        return Response(data, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({
            "error": "Lỗi khi gửi yêu cầu đến backend",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_products_by_category_plural(request, category_plural):
    # Chuyển đổi dạng số nhiều về singular keys trong SERVICE_URLS
    category_map = {
        'laptops': 'laptop',
        'books': 'book',
        'mobiles': 'mobile',
        'clothes': 'clothes',  # clothes không đổi
    }
    category = category_map.get(category_plural.lower())
    if not category:
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)
    
    base_url = SERVICE_URLS.get(category)
    if not base_url:
        return Response({"error": "Service not available"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            return Response(response.json())
        return Response({"error": "Service error"}, status=response.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
