""" KHỐI LƯỢNG (Volume / Participation)
👉 Có tiền thật vào không?
- Volume
- Volume MA
- OBV
- VWAP
- Volume Profile
📌 Dùng để xác nhận tín hiệu """

def pt_volume(df, window=20): #chien_luoc_don_bay
    """Phân tích Volume: So sánh khối lượng hiện tại với trung bình"""
    vol_now = df['volume'].iloc[-1]
    vol_mean = df['volume'].rolling(window).mean().iloc[-1]
    
    trang_thai = 'DOT_BIEN' if vol_now > vol_mean * 2 else ('TANG' if vol_now > vol_mean else 'THAP')
    
    return {
        'vol_now': vol_now,
        'vol_mean': vol_mean,
        'trang_thai': trang_thai
    }