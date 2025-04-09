import joblib
import numpy as np
import pickle
import os

# Lấy đường dẫn thư mục hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn đến mô hình và vectorizer
model_path = os.path.join(current_dir, "model", "svm_model.pkl")
vectorizer_path = os.path.join(current_dir, "model", "tfidf_vectorizer.pkl")

# Mở và tải mô hình SVM
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Mở và tải vectorizer
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

def predict_sentiment(comment):
    """Dự đoán cảm xúc của bình luận."""
    
    # Biến đổi dữ liệu đầu vào (comment)
    processed_comment = vectorizer.transform([comment])
    
    # Dự đoán kết quả
    prediction = model.predict(processed_comment)
    
    # Trả về kết quả dự đoán (NEGATIVE/POSITIVE/NEUTRAL)
    return prediction[0]
