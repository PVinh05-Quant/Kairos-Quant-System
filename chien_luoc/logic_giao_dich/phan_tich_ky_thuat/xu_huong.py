""" XU HƯỚNG (Trend)
👉 Giá đang đi hướng nào?
- EMA, SMA
- MACD
- ADX
- Ichimoku
- SuperTrend
📌 Dùng để chọn phe BUY / SELL """

from ta.trend import EMAIndicator, ADXIndicator

def pt_ema_trend(df, window=20): #chien_luoc_theo_xu_huong
    """Phân tích xu hướng dựa trên EMA: Giá trên/dưới đường trung bình"""
    ema_ind = EMAIndicator(df['close'], window=window)
    ema_val = ema_ind.ema_indicator().iloc[-1]
    price_now = df['close'].iloc[-1]
    
    trang_thai = 'TĂNG' if price_now > ema_val else 'GIẢM'
    
    return {
        'ema_val': ema_val,
        'price_now': price_now,
        'trang_thai': trang_thai,
        'muc_do': 'TỐT' if abs(price_now - ema_val) / ema_val > 0.005 else 'YẾU'
    }

def pt_adx(df, window=28):
    """Phân tích lực của xu hướng qua ADX"""
    # Bắt buộc phải có đoạn này để chống lỗi index
    if df is None or len(df) < window: 
        return {'adx_val': 0, 'trang_thai': 'SIDEWAY', 'muc_do': 'THAP'}
    
    try:
        adx_ind = ADXIndicator(df['high'], df['low'], df['close'], window=window)
        adx_val = adx_ind.adx().iloc[-1]
        trang_thai = 'CO_XU_HUONG' if adx_val > 25 else 'SIDEWAY'
        return {
            'adx_val': adx_val,
            'trang_thai': trang_thai,
            'muc_do': 'MANH' if adx_val > 40 else 'TRUNG_BINH'
        }
    except:
        return {'adx_val': 0, 'trang_thai': 'SIDEWAY', 'muc_do': 'THAP'}
