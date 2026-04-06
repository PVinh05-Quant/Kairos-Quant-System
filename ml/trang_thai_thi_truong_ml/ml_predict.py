import csv
import os
import json
from datetime import datetime
from ml.trang_thai_thi_truong_ml.ml_model import AI_Engine, DATA_DIR
from ml.trang_thai_thi_truong_ml.tao_feature import feature_dataset 
import pandas as pd

LOG_FILE = os.path.join(DATA_DIR, "trading_memory.csv")
engine = AI_Engine() 

STATE_MAP = {
    0: "Noise",             #Nhiễu (hoặc "Rác")
    1: "Trend_following",   #Có xu hướng (Trending)
    2: "Mean_reversion",    #Đi ngang (Sideways / Ranging)
    3: "Squeeze",           #Tích lũy / Nén (Consolidation)
    4: "Breakout",          #Bùng nổ (Expansion)
    5: "Scalping"           #Biến động hỗn loạn (Choppy/Volatile)
}

def du_doan_trang_thai_ml(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h):

    feature_dict = feature_dataset(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h)
    
    if feature_dict is None or (isinstance(feature_dict, pd.DataFrame) and feature_dict.empty): 
        return None

    input_vector = {k: v.iloc[-1] for k, v in feature_dict.items()}
    
    # 2. Dự đoán
    state_id, conf, probs = engine.predict(input_vector)
    
    if state_id is None: return None

    # 3. Đóng gói
    packet = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'state_id': state_id,
        'state_name': STATE_MAP.get(state_id, "UNKNOWN"),
        'confidence': round(conf, 4),
        'probs': probs,
        'features_snapshot': input_vector 
    }
    return packet

def danh_gia_ml(packet, pnl, dd, correct=None):

    if not packet: return

    if correct is None:
        correct = 'NaN'

    state_name = packet['state_name']

    if pnl > 0:
        reward = pnl * 1.0 
    else:
        reward = pnl * 2.0 

    # --- 2. ĐIỀU CHỈNH THEO CHIẾN THUẬT ---
    if state_name == 'RANGE':
        if pnl < 0: reward -= 2.0
        elif pnl > 0 and pnl < 0.5: reward += 0.5
    elif state_name == 'BREAKOUT':
        if pnl < 0: reward -= 2.0
        elif pnl > 2.0: reward += 2.0
    elif state_name == 'XU_HUONG_MANH':
        if pnl < 0: reward *= 1.5
        elif pnl > 3.0: reward += 3.0
    elif state_name == 'DAO_CHIEU':
        if pnl < -1.0: reward -= 3.0
        elif pnl > 1.5: reward += 2.0
    else:
        if dd < -1.0: reward -= 1.0

    reward = max(min(reward, 10), -10)

    # --- 3. LƯU LOG ---
    log_row = {
        'timestamp': packet['timestamp'],
        'state': packet['state_id'],      
        'correct': correct,
        'state_name': packet['state_name'],
        'confidence': packet['confidence'],
        'pnl': round(pnl, 4),
        'reward': round(reward, 4),
        'features_json': json.dumps(packet['features_snapshot'])
    }
    
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_row.keys())
        if not file_exists: writer.writeheader()
        writer.writerow(log_row)

