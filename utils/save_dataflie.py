import pandas as pd
from pathlib import Path
from datetime import datetime

def luu_du_lieu_vectorized(df, symbol, time_frame, label="backtest"):
    """
    Lưu trữ DataFrame đa khung thời gian sang định dạng CSV để mở trực tiếp bằng Excel.
    Tự động xử lý lỗi thư mục và làm sạch tên file.
    """
    try:
        # 1. Làm sạch tên Symbol (Thay SOL/USDT thành SOL_USDT)
        clean_symbol = str(symbol).replace('/', '_').replace('\\', '_').replace(':', '_')
        
        # 2. Xác định đường dẫn gốc (Lùi 1 cấp từ utils/ về thư mục gốc dự án)
        base_dir = Path(__file__).resolve().parents[1] 
        folder_path = base_dir / 'du_lieu' / 'du_lieu_vectorized' / clean_symbol
        
        # 3. Tạo thư mục duy nhất (parents=True giúp tạo cả cây thư mục nếu chưa có)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # 4. Đặt tên file CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        file_name = f"{clean_symbol}_{time_frame}_{label}_{timestamp}.csv"
        full_path = folder_path / file_name
        
        # 5. Lưu file CSV
        # index=True để giữ lại cột thời gian (Datetime Index)
        df.to_csv(full_path, index=True)
        
        print(f"✅ Đã lưu file CSV thành công!")
        print(f"📍 Đường dẫn: {full_path}")
        
        return str(full_path)

    except Exception as e:
        print(f"❌ Lỗi khi lưu file CSV: {e}")
        return None