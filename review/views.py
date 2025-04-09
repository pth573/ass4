from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from django.http import JsonResponse

# Customer and Product APIs
CUSTOMER_API_URL = "http://127.0.0.1:8000/api/customers/"
PRODUCT_API_URL = "http://127.0.0.1:8000/api/products/"

API_ENDPOINTS = {
    "mobile": "http://127.0.0.1:8000/api/mobiles/mobiles/",
    "laptop": "http://127.0.0.1:8000/api/laptops/laptops/",
    "clothes": "http://127.0.0.1:8000/api/clothes/clothes/",
    "book": "http://127.0.0.1:8000/api/books/books/",
}

# Get a list of all reviews
@api_view(['GET'])
def get_all_reviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# Get reviews by customer_id
@api_view(['GET'])
def get_reviews_by_customer(request, customer_id):
    reviews = Review.objects.filter(customer_id=customer_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# Get reviews by product_id and category
@api_view(['GET'])
def get_reviews_by_product(request, category, product_id):
    if category not in API_ENDPOINTS:
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)
    
    product_url = f"{API_ENDPOINTS[category]}{product_id}/"
    product_response = requests.get(product_url)

    if product_response.status_code != 200:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    product_data = product_response.json()
    reviews = Review.objects.filter(product_id=product_id, category=category)
    serializer = ReviewSerializer(reviews, many=True)

    return Response({
        "product": product_data,
        "reviews": serializer.data
    })

# Add new review
@api_view(['POST'])
def add_review(request):
    customer_id = request.data.get("customer_id")
    category = request.data.get("category")
    product_id = request.data.get("product_id")

    if category not in API_ENDPOINTS:
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)

    customer_response = requests.get(f"{CUSTOMER_API_URL}{customer_id}/")
    if customer_response.status_code != 200:
        return Response({"error": "Invalid customer ID"}, status=status.HTTP_400_BAD_REQUEST)

    customer_data = customer_response.json()

    product_response = requests.get(f"{API_ENDPOINTS[category]}{product_id}/")
    if product_response.status_code != 200:
        return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)

    product_data = product_response.json()
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        review = serializer.save()
        return Response({
            "review_id": review.id,
            "customer": customer_data,
            "product": product_data,
            "category": review.category,
            "rating": review.rating,
            "comment": review.comment
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get full review information with customer & product
@api_view(['GET'])
def get_full_reviews(request):
    reviews = Review.objects.all()
    review_list = []

    for review in reviews:
        customer_response = requests.get(f"{CUSTOMER_API_URL}{review.customer_id}/")
        customer_data = customer_response.json() if customer_response.status_code == 200 else None

        product_url = f"{API_ENDPOINTS.get(review.category, '')}{review.product_id}/"
        product_response = requests.get(product_url)
        product_data = product_response.json() if product_response.status_code == 200 else None

        review_list.append({
            "review_id": review.id,
            "customer": customer_data,
            "product": product_data,
            "category": review.category,
            "rating": review.rating,
            "comment": review.comment
        })

    return Response(review_list)

# Get review by id
@api_view(['GET'])
def get_review_by_id(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

# Analyze customer reviews
def analyze_customer_reviews(request, customer_id):
    reviews = Review.objects.filter(customer_id=customer_id)
    sentiments = []

    for review in reviews:
        response = requests.post(
            "http://127.0.0.1:8000/api/review-analysis/analyze/",
            json={"comment": review.comment},
        )

        if response.status_code == 200:
            sentiments.append({"comment": review.comment, "sentiment": response.json()["sentiment"]})

    return JsonResponse({"customer_id": customer_id, "reviews": sentiments})

# Analyze review by id
@api_view(['GET'])
def analyze_review_by_id(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        response = requests.post(
            "http://127.0.0.1:8000/api/review-analysis/analyze/",
            json={"comment": review.comment},
        )

        if response.status_code == 200:
            sentiment = response.json().get("sentiment")
            return JsonResponse({"review_id": review_id, "comment": review.comment, "sentiment": sentiment})
        else:
            return JsonResponse({"error": "Sentiment analysis failed"}, status=500)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found"}, status=404)
