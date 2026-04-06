﻿import joblib
import os
from sklearn.metrics import precision_score, recall_score, f1_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCALER_PATH = os.path.join(BASE_DIR, 'du_lieu', 'scaler.pkl')

def luu_scaler(scaler):
    joblib.dump(scaler, SCALER_PATH)
    print(f"💾 Đã lưu bộ chuẩn hóa dữ liệu (Scaler) tại: {SCALER_PATH}")

def tai_scaler():
    if os.path.exists(SCALER_PATH):
        return joblib.load(SCALER_PATH)
    return None
