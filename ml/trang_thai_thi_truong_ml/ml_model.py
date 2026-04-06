import os
import json
import random
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from .tao_feature import feature_dataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

FILE_PATH = Path(__file__).resolve()
ROOT_DIR = FILE_PATH.parent.parent.parent
for parent in FILE_PATH.parents:
    if (parent / 'du_lieu_ml').exists():
        ROOT_DIR = parent
        break

DATA_DI = os.path.join(ROOT_DIR, 'trang_thai_thi_truong_ml')
DATA_DIR = os.path.join(ROOT_DIR, 'du_lieu_ml')

MODEL_PATH = os.path.join(DATA_DIR, 'model_pytorch.pth') 
SCALER_PATH = os.path.join(DATA_DIR, 'scaler_params.json')
INFO_PATH = os.path.join(DATA_DIR, 'model_info.json')

class MyTorchScaler:
    def __init__(self):
        self.mean = None
        self.std = None
    
    def fit(self, x_tensor):
        self.mean = x_tensor.mean(dim=0).cpu()
        self.std = x_tensor.std(dim=0).cpu()
        self.std[self.std == 0] = 1e-7 # Tránh chia cho 0
        
    def transform(self, x_tensor):
        if self.mean is None: raise ValueError("Scaler chưa fit!")
        return (x_tensor - self.mean.to(x_tensor.device)) / self.std.to(x_tensor.device)
        
    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'mean': self.mean.tolist(), 'std': self.std.tolist()}, f)
            
    def load(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        self.mean = torch.tensor(data['mean'])
        self.std = torch.tensor(data['std'])

class ResBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(dim, dim),
            nn.BatchNorm1d(dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(dim, dim),
            nn.BatchNorm1d(dim)
        )
    def forward(self, x):
        return torch.relu(x + self.block(x))

class TradingMLP(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(TradingMLP, self).__init__()
        self.input_layer = nn.Sequential(nn.Linear(input_dim, 256), nn.BatchNorm1d(256), nn.ReLU())

        self.res_blocks = nn.Sequential(
            ResBlock(256),
            ResBlock(256),
            ResBlock(256)
        )
        
        self.output_layer = nn.Sequential(
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        x = self.input_layer(x)
        x = self.res_blocks(x)
        return self.output_layer(x)

class AI_Engine:
    def __init__(self, model_path=MODEL_PATH):
        self.model = None
        self.scaler = None
        self.feature_names = [] 
        self.load(model_path)

    def load(self, model_path):
        try:
            if not os.path.exists(model_path) or not os.path.exists(SCALER_PATH): 
                return
            
            with open(INFO_PATH, 'r') as f: info = json.load(f)
            self.feature_names = info.get('feature_names', [])
            input_dim = info['input_dim']

            self.model = TradingMLP(input_dim, info['output_dim']).to(device)

            self.model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
            self.model.eval()
            self.scaler = MyTorchScaler()
            self.scaler.load(SCALER_PATH)
            #print(f"✅ AI Engine Loaded: {os.path.basename(model_path)} (Input: {input_dim}) on {device}")
        except Exception as e: print(f"❌ Load Error: {e}")

    def predict(self, feature_vector_dict, explore=True):
        if not self.model: 
            return None, 0.0, None

        vals = []
        for name in self.feature_names:
            vals.append(feature_vector_dict.get(name, 0.0))

        x_tensor = torch.tensor(vals, dtype=torch.float32).unsqueeze(0).to(device)

        with torch.no_grad():
            x_scaled = self.scaler.transform(x_tensor)
            logits = self.model(x_scaled)
            probs = torch.softmax(logits, dim=1)[0]
            conf, pred_class = torch.max(probs, 0)

        # 🔥 RANDOM EXPLORATION (Epsilon-Greedy) 🔥
        if explore and conf.item() < 0.2: #20% ngẫu nhiên   
            pred_class = torch.tensor(random.randint(0, probs.shape[0]-1)).to(device)
            conf = torch.tensor(0.1).to(device)

        return int(pred_class.item()), float(conf.item()), probs.tolist()

# --- 5. HÀM HUẤN LUYỆN
def huan_luyen_model(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h):
    os.makedirs(DATA_DIR, exist_ok=True)
    log_path = os.path.join(DATA_DIR, "trading_memory.csv")
    
    X_list, y_list = [], []
    VALID_FEATURES = []

    # --- TRƯỜNG HỢP 1: NẾU ĐÃ CÓ DỮ LIỆU KINH NGHIỆM (LOG) ---
    if os.path.exists(log_path):
        try:
            df_log = pd.read_csv(log_path)
            if len(df_log) >= 10:
                print(f"🧠 Phát hiện {len(df_log)} mẫu kinh nghiệm. AI đang học từ thực tế...")
                for _, row in df_log.iterrows():
                    try:
                        feats = json.loads(row['features_json'])
                        X_list.append(list(feats.values()))
                        
                        label = int(row['correct']) if pd.notna(row['correct']) else int(row['state'])
                        y_list.append(label)
                        
                        if not VALID_FEATURES: VALID_FEATURES = list(feats.keys())
                    except: continue
        except Exception as e:
            print(f"❌ Lỗi đọc log: {e}")

    # --- TRƯỜNG HỢP 2: KHÔNG CÓ LOG -> KHỞI TẠO BẰNG TỶ LỆ ĐỀU NHAU ---
    if len(X_list) < 10:
        print("⚠️ Không có dữ liệu log. Tiến hành khởi tạo 'Bộ não trắng' với tỷ lệ nhãn đều nhau...")
        feats = feature_dataset(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h)
        if feats is None or feats.empty: return
        
        df_feat = pd.DataFrame(feats).ffill().fillna(0.0)
        n_samples = len(df_feat)
        
        X_list = df_feat.values.tolist()
        VALID_FEATURES = df_feat.columns.tolist()

        y_list = np.tile([0, 1, 2, 3, 4, 5], (n_samples // 6) + 1)[:n_samples].tolist()

    X_tensor = torch.tensor(X_list, dtype=torch.float32)
    y_tensor = torch.tensor(y_list, dtype=torch.long).to(device)

    scaler = MyTorchScaler()
    scaler.fit(X_tensor)
    X_train_scaled = scaler.transform(X_tensor).to(device)
    scaler.save(SCALER_PATH)

    INPUT_DIM = X_train_scaled.shape[1]
    OUTPUT_DIM = 6
    model = TradingMLP(INPUT_DIM, OUTPUT_DIM).to(device)
    
    optimizer = optim.AdamW(model.parameters(), lr=0.001)

    counts = np.bincount(y_list, minlength=6)
    weights = torch.tensor((1.0 / (counts + 1)) / (1.0 / (counts + 1)).sum() * 6, dtype=torch.float32).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights)

    print(f"🚀 Đang huấn luyện bộ lọc trên {len(X_list)} mẫu (Device: {device})...")
    model.train()
    for epoch in range(50):
        optimizer.zero_grad()
        outputs = model(X_train_scaled)
        loss = criterion(outputs, y_tensor)
        loss.backward()
        optimizer.step()

    torch.save(model.state_dict(), MODEL_PATH)
    with open(INFO_PATH, 'w') as f:
        json.dump({
            'input_dim': INPUT_DIM,
            'output_dim': OUTPUT_DIM,
            'feature_names': VALID_FEATURES 
        }, f)
        
    print(f"✅ Đã cập nhật xong Bộ lọc AI. Model sẵn sàng chạy (Input: {INPUT_DIM}).")

def tu_dong_hoc_tu_log():
    log_path = os.path.join(DATA_DIR, "trading_memory.csv")
    if not os.path.exists(log_path): return

    print("🧠 Đang ôn bài từ kinh nghiệm thực chiến...")
    try:
        df_log = pd.read_csv(log_path)
    except Exception as e: return
    
    # Lọc các ký ức tốt và xấu
    good_memories = df_log[df_log['reward'] > 0.0].copy()
    bad_memories = df_log[df_log['reward'] < 0.0].copy()
    
    if len(good_memories) + len(bad_memories) < 10: return

    X_list, y_list = [], []

    # 1. Xử lý ký ức tốt
    for _, row in good_memories.iterrows():
        try:
            feats = json.loads(row['features_json']) if isinstance(row['features_json'], str) else row['features_json']
            X_list.append(list(feats.values()))
            y_list.append(int(row['state'])) 
        except: continue

    # 2. Xử lý ký ức xấu (sửa sai)
    if len(bad_memories) > 0:
        for _, row in bad_memories.iterrows():
            try:
                feats = json.loads(row['features_json']) if isinstance(row['features_json'], str) else row['features_json']
                wrong_state = int(row['state'])
                corrected_state = wrong_state 

                has_teacher = 'correct' in row and pd.notna(row['correct']) and row['correct'] != ''
                if has_teacher:
                    corrected_state = int(row['correct'])
                else:
                    # Logic tự sửa sai cơ bản nếu không có thầy giáo
                    if wrong_state in [0, 1, 3]: corrected_state = 2 
                    elif wrong_state == 2: corrected_state = 0 
                    elif wrong_state == 5: corrected_state = 0

                if corrected_state != wrong_state:
                    X_list.append(list(feats.values()))
                    y_list.append(corrected_state)
            except: continue

    if not X_list: return

    # Chuyển sang Tensor
    X_train = torch.tensor(X_list, dtype=torch.float32)
    y_train = torch.tensor(y_list, dtype=torch.long).to(device)

    # --- KHỞI TẠO ENGINE ---
    # Lưu ý: Không cần import lại AI_Engine vì đang ở trong cùng file
    engine = AI_Engine() 
    
    # --- KIỂM TRA KHỚP DỮ LIỆU (FIX LỖI 72 vs 120) ---
    input_dim_new = X_train.shape[1]
    input_dim_old = 0
    
    # Lấy kích thước của Scaler cũ nếu có
    if engine.scaler is not None and engine.scaler.mean is not None:
        input_dim_old = engine.scaler.mean.shape[0]

    model = None
    scaler = None
    
    # Nếu dữ liệu mới khác kích thước dữ liệu cũ -> RESET MODEL & SCALER
    if input_dim_new != input_dim_old:
        print(f"⚠️ Phát hiện thay đổi dữ liệu (Cũ: {input_dim_old} -> Mới: {input_dim_new}). Tiến hành huấn luyện lại từ đầu...")
        
        # Tạo Scaler mới và fit ngay lập tức với dữ liệu hiện tại
        scaler = MyTorchScaler()
        scaler.fit(X_train)
        
        # Tạo Model mới tương ứng với input_dim mới
        model = TradingMLP(input_dim_new, 6).to(device) # Giả sử output là 6 lớp
        
        # Gán lại vào engine để tí nữa dùng
        engine.model = model
        engine.scaler = scaler
        
        # Cập nhật lại file info để lần sau load đúng
        with open(INFO_PATH, 'w') as f:
            # Lấy tên feature từ dòng đầu tiên của log (nếu có thể) để lưu lại tên cột
            feature_names_new = []
            try:
                first_row_feat = json.loads(good_memories.iloc[0]['features_json'])
                feature_names_new = list(first_row_feat.keys())
            except: pass
            
            json.dump({
                'input_dim': input_dim_new,
                'output_dim': 6,
                'feature_names': feature_names_new 
            }, f)
            
    else:
        # Nếu khớp dimension thì dùng tiếp model/scaler cũ
        print(f"✅ Dữ liệu khớp ({input_dim_new} features). Đang tinh chỉnh model...")
        model = engine.model
        scaler = engine.scaler

    # --- TIẾN HÀNH TRAINING ---
    model.train() 
    optimizer = optim.Adam(model.parameters(), lr=0.0001) 
    criterion = nn.CrossEntropyLoss()

    # --- CHUẨN BỊ DỮ LIỆU CHIA BATCH ---
    # CHÚ Ý: Tạm thời giữ dữ liệu ở CPU, KHÔNG dùng .to(device) ở đây để tránh tràn RAM GPU
    X_train_scaled = scaler.transform(X_train).cpu() 
    y_train_cpu = y_train.cpu()

    # Khởi tạo DataLoader để chia nhỏ dữ liệu
    # Nếu vẫn bị lỗi OOM, hãy giảm batch_size xuống 128 hoặc 64
    batch_size = 256 
    dataset = TensorDataset(X_train_scaled, y_train_cpu)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # --- TIẾN HÀNH TRAINING THEO BATCH ---
    model.train() 
    optimizer = optim.Adam(model.parameters(), lr=0.0001) 
    criterion = nn.CrossEntropyLoss()

    for epoch in range(10): # Train 10 epoch
        total_loss = 0.0
        for batch_X, batch_y in dataloader:
            # Chỉ đưa từng gói dữ liệu nhỏ (256 dòng) lên GPU
            batch_X = batch_X.to(device)
            batch_y = batch_y.to(device)

            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        print(f"  + Epoch {epoch+1}/10 - Loss: {total_loss/len(dataloader):.4f}")

    # --- LƯU LẠI MODEL VÀ SCALER MỚI ---
    torch.save(model.state_dict(), MODEL_PATH)
    scaler.save(SCALER_PATH) 
    
    print(f"✅ Đã học xong {len(X_list)} bài học mới trên GPU (Input: {input_dim_new}).")