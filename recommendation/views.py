# from django.shortcuts import render

# # Create your views here.
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import requests
# import numpy as np
# import pandas as pd
# from sklearn.neighbors import NearestNeighbors

# # URL API
# REVIEW_API_URL = "http://127.0.0.1:8000/api/reviews/"
# ANALYSIS_API_URL = "http://127.0.0.1:8000/api/review-analysis/analyze/"
# # PRODUCT_API_URL = "http://127.0.0.1:8000/api/products/{category}/{product_id}/"
# PRODUCT_API_URL = "http://127.0.0.1:8000/api/products/{category}s/{product_id}/"


# def calculate_preference_score(sentiment_label):
#     """Convert sentiment to Preference Score (1-5)."""
#     sentiment_mapping = {
#         "POSITIVE": 5,
#         "NEUTRAL": 3,
#         "NEGATIVE": 1
#     }
#     return sentiment_mapping.get(sentiment_label, 3)  # Defaults to NEUTRAL if not found

# @csrf_exempt
# def recommend_products(request, customer_id):
#     """Product recommendation based on sentiment and Collaborative Filtering (KNN)."""
    
#     # Get customer reviews
#     response = requests.get(f"{REVIEW_API_URL}customer/{customer_id}/")
#     if response.status_code != 200:
#         return JsonResponse({"error": "Customer reviews not found"}, status=404)
    
#     reviews = response.json()
#     scores = []
#     product_details = {}

#     # Convert Sentiment to Preference Score
#     for review in reviews:
#         sentiment_response = requests.post(ANALYSIS_API_URL, json={"comment": review["comment"]})
#         if sentiment_response.status_code == 200:
#             sentiment_label = sentiment_response.json().get("sentiment", "NEUTRAL")  # Defaults to NEUTRAL if error
#             preference_score = calculate_preference_score(sentiment_label)
            
#             product_id = review["product_id"]
#             category = review["category"]
            
#             # Get product information from API
#             product_response = requests.get(PRODUCT_API_URL.format(category=category, product_id=product_id))
#             if product_response.status_code == 200:
#                 product_info = product_response.json()
#                 product_details[(product_id, category)] = product_info  # Save product information
            
#             scores.append((product_id, category, preference_score))

#     if not scores:
#         return JsonResponse({"error": "No recommendations available"}, status=404)

#     # Create User-Product matrix
#     df = pd.DataFrame(scores, columns=["product_id", "category", "score"])

#     # Keep both `product_id` and `category` as indexes
#     user_product_matrix = df.pivot_table(index=["product_id", "category"], values="score", aggfunc="mean").fillna(0)

#     # Using KNN with Cosine Similarity
#     knn_model = NearestNeighbors(metric="cosine", algorithm="brute")
#     knn_model.fit(user_product_matrix)

#     # Select customer reviewed products, keeping both `product_id` and `category`
#     reviewed_products = df[["product_id", "category"]].drop_duplicates().values.tolist()

#     recommendations = []
#     for product_id, category in reviewed_products:
#         try:
#             product_index = list(user_product_matrix.index).index((product_id, category))
#             distances, indices = knn_model.kneighbors([user_product_matrix.iloc[product_index]], n_neighbors=2)

#             for i in range(1, len(indices[0])):  # Skip original products
#                 rec_product_id, rec_category = user_product_matrix.index[indices[0][i]]
#                 recommendations.append(((rec_product_id, rec_category), 1 / distances[0][i]))  # Invert distances to similarities
#         except Exception as e:
#             continue

#     # Sort & get Top 5
#     recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

#     recommended_products = []
#     for (pid, category), score in recommendations:
#         # Call API to get product information
#         product_response = requests.get(PRODUCT_API_URL.format(category=category, product_id=pid))
#         if product_response.status_code == 200:
#             product_info = product_response.json()
#             recommended_products.append({
#                 "product_id": int(pid),
#                 "category": category,
#                 "product_name": product_info.get("name", "Unknown"),
#                 "price": product_info.get("price", 0),
#                 "similarity_score": round(float(score), 2)
#             })

#     return JsonResponse({"customer_id": customer_id, "recommendations": recommended_products})





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# API URLs
REVIEW_API_URL = "http://127.0.0.1:8000/api/reviews/"
ANALYSIS_API_URL = "http://127.0.0.1:8000/api/review-analysis/analyze/"
PRODUCT_API_URL = "http://127.0.0.1:8000/api/products/{category}s/{product_id}/"

def calculate_preference_score(sentiment_label):
    """Chuyển đổi sentiment thành điểm ưu tiên (1-5)."""
    sentiment_mapping = {
        "POSITIVE": 5,
        "NEUTRAL": 3,
        "NEGATIVE": 1
    }
    return sentiment_mapping.get(sentiment_label, 3)

@csrf_exempt
def recommend_products(request, customer_id):
    """Đề xuất sản phẩm dựa vào cảm xúc và Collaborative Filtering."""

    # Lấy các đánh giá của khách hàng
    response = requests.get(f"{REVIEW_API_URL}customer/{customer_id}/")
    if response.status_code != 200:
        return JsonResponse({"error": "Customer reviews not found"}, status=404)

    reviews = response.json()
    scores = []
    product_details = {}

    # Chuyển đổi cảm xúc thành điểm
    for review in reviews:
        sentiment_response = requests.post(ANALYSIS_API_URL, json={"comment": review["comment"]})
        if sentiment_response.status_code == 200:
            sentiment_label = sentiment_response.json().get("sentiment", "NEUTRAL")
            preference_score = calculate_preference_score(sentiment_label)

            product_id = review["product_id"]
            category = review["category"]

            # Lấy thông tin sản phẩm
            product_response = requests.get(PRODUCT_API_URL.format(category=category, product_id=product_id))
            if product_response.status_code == 200:
                product_info = product_response.json()
                product_details[(product_id, category)] = product_info

            scores.append((product_id, category, preference_score))

    if not scores:
        return JsonResponse({"error": "No recommendations available"}, status=404)

    # Tạo ma trận User-Product
    df = pd.DataFrame(scores, columns=["product_id", "category", "score"])
    user_product_matrix = df.pivot_table(index=["product_id", "category"], values="score", aggfunc="mean").fillna(0)

    # Huấn luyện mô hình KNN
    knn_model = NearestNeighbors(metric="cosine", algorithm="brute")
    knn_model.fit(user_product_matrix.to_numpy())  # Sử dụng numpy array để tránh warning

    reviewed_products = df[["product_id", "category"]].drop_duplicates().values.tolist()

    recommendations = set()
    similarity_map = {}

    for idx, (product_id, category) in enumerate(reviewed_products):
        try:
            product_index = list(user_product_matrix.index).index((product_id, category))
            distances, indices = knn_model.kneighbors(
                [user_product_matrix.iloc[product_index].to_numpy()],
                n_neighbors=6
            )

            for i in range(1, len(indices[0])):  # Bỏ qua chính nó
                rec_index = indices[0][i]
                distance = distances[0][i]

                # Tránh chia cho 0
                if distance == 0:
                    similarity = 1.0
                else:
                    similarity = round(1 / distance, 2)

                rec_product_id, rec_category = user_product_matrix.index[rec_index]

                # Tránh đề xuất chính sản phẩm đã xem
                if (rec_product_id, rec_category) not in reviewed_products:
                    recommendations.add((rec_product_id, rec_category))
                    similarity_map[(rec_product_id, rec_category)] = similarity
        except Exception:
            continue

    # Lấy Top 5
    sorted_recommendations = sorted(
        recommendations,
        key=lambda x: similarity_map.get(x, 0),
        reverse=True
    )[:5]

    recommended_products = []
    for pid, category in sorted_recommendations:
        product_response = requests.get(PRODUCT_API_URL.format(category=category, product_id=pid))
        if product_response.status_code == 200:
            product_info = product_response.json()
            recommended_products.append({
                "product_id": int(pid),
                "category": category,
                "product_name": product_info.get("name", "Unknown"),
                "price": product_info.get("price", 0),
                "similarity_score": similarity_map.get((pid, category), 0)
            })

    return JsonResponse({
        "customer_id": customer_id,
        "recommendations": recommended_products
    })
