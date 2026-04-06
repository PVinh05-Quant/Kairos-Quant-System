import json
import os
from utils.log import logger
from PyQt6.QtCore import QObject, pyqtSignal


class SignalManager(QObject):
    data_changed = pyqtSignal(dict)

ui_signals = SignalManager()
# --- ĐƯỜNG DẪN FILE ---
FILE_REALTIME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'du_lieu', 'thong_tin_lenh', 'trang_thai_lenh_realtime.json')
FILE_DEMO = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'du_lieu', 'thong_tin_lenh', 'trang_thai_lenh_demo.json')

FILE_LICH_SU_REALTIME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'du_lieu', 'thong_tin_lenh', 'lich_su_lenh_realtime.json')
FILE_LICH_SU_DEMO = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'du_lieu', 'thong_tin_lenh', 'lich_su_lenh_demo.json')

# --- BIẾN TOÀN CỤC ---
danh_sach_lenh_dang_chay = {}
data_lenh_dang_chay = {}
data_lich_su = [] 

MAX_CANDLES_MEMORY = 300
total_lenh_lich_su = 100 

def get_all_data():
    """Hàm gom toàn bộ dữ liệu hiện tại để gửi đi"""
    return {
        "lenh_dang_chay": danh_sach_lenh_dang_chay,
        "data_lenh_dang_chay": data_lenh_dang_chay,
        "lich_su": list(data_lich_su)
    }

def load_trang_thai(CHUC_NANG):
    """Load dữ liệu từ file vào RAM"""
    if CHUC_NANG == 'realtime':      
        file_dang_chay = FILE_REALTIME
        file_lich_su   = FILE_LICH_SU_REALTIME
    elif CHUC_NANG == 'demo':           
        file_dang_chay = FILE_DEMO
        file_lich_su   = FILE_LICH_SU_DEMO
    else: return

    # 1. Load lệnh đang chạy
    if os.path.exists(file_dang_chay):
        try:
            with open(file_dang_chay, 'r', encoding='utf-8') as f:
                data = json.load(f)
                danh_sach_lenh_dang_chay.clear()
                danh_sach_lenh_dang_chay.update(data)
            logger.info(f" [{CHUC_NANG}] 📂 Đã khôi phục {len(danh_sach_lenh_dang_chay)} lệnh đang treo.")
        except Exception as e:
            logger.error(f"Lỗi load đang chạy: {e}")

    # 2. Load lịch sử
    if os.path.exists(file_lich_su):
        try:
            with open(file_lich_su, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            last_100 = lines[-100:] if len(lines) > 100 else lines
            
            data_lich_su.clear() # Xóa dữ liệu cũ

            for line in last_100:
                line = line.strip()
                if not line: continue
                try:
                    order = json.loads(line)
                    data_lich_su.append(order) # Append vào List
                except: continue
            
            logger.info(f" [{CHUC_NANG}] 📜 Đã khôi phục {len(data_lich_su)} dòng lịch sử.")
        except Exception as e:
            logger.error(f"Lỗi load lịch sử: {e}")

    ui_signals.data_changed.emit(get_all_data())

def lich_su_lenh(CHUC_NANG, order_info):
    if CHUC_NANG == 'realtime':
        file_path = FILE_LICH_SU_REALTIME
    elif CHUC_NANG == 'demo':
        file_path = FILE_LICH_SU_DEMO
    else:
        return
    
    data_lich_su.append(order_info)

    while len(data_lich_su) > total_lenh_lich_su:
        data_lich_su.pop(0)

    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            json_line = json.dumps(order_info, ensure_ascii=False)
            f.write(json_line + '\n')
        ui_signals.data_changed.emit(get_all_data())
    except Exception as e:
        if 'logger' in globals():
            logger.error(f"Lỗi ghi file lịch sử ({CHUC_NANG}): {e}")
        else:
            print(f"Lỗi: {e}")

def save_trang_thai(CHUC_NANG):
    if CHUC_NANG == 'realtime':
        file_path = FILE_REALTIME
    elif CHUC_NANG == 'demo':
        file_path = FILE_DEMO
    else: return

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(danh_sach_lenh_dang_chay, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Lỗi lưu file trạng thái: {e}")

def luu_lenh_moi(CHUC_NANG, symbol, order_info):
    danh_sach_lenh_dang_chay[symbol] = order_info
    save_trang_thai(CHUC_NANG)
    ui_signals.data_changed.emit(get_all_data())

def xoa_lenh(CHUC_NANG, symbol):
    if symbol in danh_sach_lenh_dang_chay:
        del danh_sach_lenh_dang_chay[symbol]

        if symbol in data_lenh_dang_chay:
            del data_lenh_dang_chay[symbol]
            
        save_trang_thai(CHUC_NANG)
        ui_signals.data_changed.emit(get_all_data())
    xoa_bien_theo_symbol(symbol)

def lay_thong_tin_lenh(symbol):
     return danh_sach_lenh_dang_chay.get(symbol)

def kiem_tra_ton_tai(symbol):
    return symbol in danh_sach_lenh_dang_chay

def lay_danh_sach_symbol_dang_co():
    return list(danh_sach_lenh_dang_chay.keys())

def data_vi_the_update(symbol, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d):
    data_lenh_dang_chay[symbol] = {
        'df_1m': df_1m.tail(MAX_CANDLES_MEMORY).copy(),
        'df_3m': df_3m.tail(MAX_CANDLES_MEMORY).copy(),
        'df_5m': df_5m.tail(MAX_CANDLES_MEMORY).copy(),
        'df_15m': df_15m.tail(MAX_CANDLES_MEMORY).copy(),
        'df_30m': df_30m.tail(MAX_CANDLES_MEMORY).copy(),
        'df_1h': df_1h.tail(MAX_CANDLES_MEMORY).copy(),
        'df_4h': df_4h.tail(MAX_CANDLES_MEMORY).copy(),
        'df_1d': df_1d.tail(MAX_CANDLES_MEMORY).copy()
    }

    ui_signals.data_changed.emit(get_all_data())
    return data_lenh_dang_chay[symbol]

def xoa_bien_theo_symbol(symbol):
    if symbol in danh_sach_lenh_dang_chay:
        del danh_sach_lenh_dang_chay[symbol]
    if symbol in data_lenh_dang_chay:
        del data_lenh_dang_chay[symbol]
    ui_signals.data_changed.emit(get_all_data())
