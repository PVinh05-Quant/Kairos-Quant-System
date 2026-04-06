""" ĐẢO CHIỀU / ĐỘNG LƯỢNG (Momentum / Reversal)
👉 Lực đang yếu đi hay mạnh lên?
- RSI
- Stochastic
- CCI
- Williams %R
- ROC
📌 Dùng để timing entry / exit """

from ta.momentum import RSIIndicator

def pt_rsi(df, window=14): #chien_luoc_theo_xu_huong
    """Phân tích sức mạnh xu hướng qua RSI"""
    rsi_ind = RSIIndicator(df['close'], window=window)
    rsi_val = rsi_ind.rsi().iloc[-1]
    
    if rsi_val > 60: trang_thai = 'MẠNH'
    elif rsi_val < 40: trang_thai = 'YẾU'
    else: trang_thai = 'TRUNG_TÍNH'
    
    return {
        'rsi_val': rsi_val,
        'trang_thai': trang_thai,
        'muc_do': 'QUÁ_MUA' if rsi_val > 70 else ('QUÁ_BÁN' if rsi_val < 30 else 'THƯỜNG')
    }