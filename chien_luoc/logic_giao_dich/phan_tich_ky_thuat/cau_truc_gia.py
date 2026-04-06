"""CẤU TRÚC GIÁ (Market Structure / Price Action) ⭐
👉 Thị trường đang ở pha nào?
- Không phải indicator cổ điển, mà là logic
- Higher High / Higher Low
- Break of Structure (BOS)
- Change of Character (CHoCH)
- Support / Resistance
- Supply / Demand
📌 Dùng để:
- Xác định trend thật
- Tránh nhiễu indicator
- Bot chuyên nghiệp luôn có nhóm này"""

def pt_breakout(df, window=20): #chien_luoc_don_bay
    """Phân tích Price Action: Phá vỡ đỉnh/đáy"""
    close_now = df['close'].iloc[-1]
    high_max = df['high'].shift(1).rolling(window).max().iloc[-1]
    low_min = df['low'].shift(1).rolling(window).min().iloc[-1]
    
    if close_now > high_max:
        trang_thai = 'BREAK_OUT'
    elif close_now < low_min:
        trang_thai = 'BREAK_DOWN'
    else:
        trang_thai = 'KHONG'
        
    return {
        'close': close_now,
        'high_max': high_max,
        'low_min': low_min,
        'trang_thai': trang_thai
    }