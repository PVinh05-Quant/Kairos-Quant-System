"""BIẾN ĐỘNG (Volatility)
👉 Giá chạy mạnh hay yếu?
- ATR
- Bollinger Bands
- Keltner Channel
- Donchian Channel
📌 Dùng cho SL / TP / leverage """

from ta.volatility import BollingerBands
from ta.volatility import AverageTrueRange

def pt_atr(df, window=14, mean_window=100):  # Chiến lược đòn bẩy, stoploss_takeprofit, chien_luoc_theo_xu_huong
    """Phân tích ATR: Mức độ biến động thị trường"""
    atr_ind = AverageTrueRange(df['high'], df['low'], df['close'], window=window)
    atr_series = atr_ind.average_true_range()

    atr_now = atr_series.iloc[-1]
    atr_mean = atr_series.rolling(mean_window).mean().iloc[-1]

    trang_thai = 'BIẾN_ĐỘNG_CAO' if atr_now > atr_mean else 'BIẾN_ĐỘNG_THẤP'

    return {
        'atr_val': atr_now,
        'atr_mean': atr_mean,
        'trang_thai': trang_thai,
        'muc_do': 'CAO' if atr_now > atr_mean else 'THAP'
    }


def pt_bollinger_squeeze(df, window=20, window_dev=2):  #chien_luoc_don_bay, #chien_luoc_dao_chieu
    """Phân tích Bollinger Bands: Trả về cả độ nén và giá trị các biên"""
    bb = BollingerBands(df['close'], window=window, window_dev=window_dev)
    
    # Lấy giá trị biên tại nến cuối cùng
    upper_band = bb.bollinger_hband().iloc[-1]
    lower_band = bb.bollinger_lband().iloc[-1]
    mid_band = bb.bollinger_mavg().iloc[-1]
    
    # Tính toán độ nén (Bandwidth)
    w_band = (bb.bollinger_hband() - bb.bollinger_lband()) / bb.bollinger_mavg()
    w_band_val = w_band.iloc[-1]
    w_band_mean = w_band.rolling(50).mean().iloc[-1] 

    return {
        'upper_band': upper_band,  # Bổ sung thêm để khớp với hàm đảo chiều
        'lower_band': lower_band,  # Bổ sung thêm để khớp với hàm đảo chiều
        'mid_band': mid_band,
        'bandwidth': w_band_val,
        'trang_thai': 'BOP' if w_band_val < w_band_mean * 0.8 else 'MO_RONG',
        'muc_do': 'CHAT' if w_band_val < w_band_mean * 0.6 else 'THUONG'
    }