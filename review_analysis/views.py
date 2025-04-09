from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .sentiment_model import predict_sentiment

@csrf_exempt
def analyze_review(request):
    if request.method == "POST":
        try:
            # Tải dữ liệu từ body của yêu cầu
            data = json.loads(request.body)
            
            # Lấy bình luận từ dữ liệu
            comment = data.get("comment", "")
            
            # Kiểm tra xem bình luận có tồn tại hay không
            if not comment:
                return JsonResponse({"error": "Comment is required"}, status=400)

            # Dự đoán cảm xúc từ bình luận
            sentiment = predict_sentiment(comment)

            # Trả về kết quả dự đoán
            return JsonResponse({"sentiment": sentiment})

        except Exception as e:
            # Xử lý lỗi bất kỳ
            return JsonResponse({"error": str(e)}, status=500)
    
    # Nếu phương thức không phải POST
    return JsonResponse({"error": "Invalid request method"}, status=405)
