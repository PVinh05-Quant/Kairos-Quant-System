from utils.log import logger
from chien_luoc.logic_giao_dich.phan_tich_ky_thuat.xu_huong import pt_adx
from chien_luoc.logic_giao_dich.phan_tich_ky_thuat.khoi_luong import pt_volume
from chien_luoc.logic_giao_dich.phan_tich_ky_thuat.cau_truc_gia import pt_breakout
from chien_luoc.logic_giao_dich.phan_tich_ky_thuat.bien_dong import pt_atr, pt_bollinger_squeeze

#df_1m có 300 nến, df_3m có 100 nến, df_5m có 300 nến, df_15m có 100 nến, df_30m có 300 nến, df_1h có 150 nến, df_4h có 300 nến, df_1d có 50 nến
def phan_tich_don_bay(symbol, don_bay, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d):
    # Khởi tạo các thông số từ chỉ báo (Dùng khung 15m làm chuẩn theo ý bạn)
    adx = pt_adx(df_15m)
    vol = pt_volume(df_15m)
    brk = pt_breakout(df_15m)
    atr = pt_atr(df_15m, 14, 100)
    bb = pt_bollinger_squeeze(df_15m)
    
    don_bay_moi = don_bay
    ly_do = ""

    # --- LOGIC ĐỊNH NGHĨA ĐIỀU KIỆN THỊ TRƯỜNG ---

    # 1. TIN MẠNH (High Volatility)
    # Đặc điểm: ATR tăng vọt so với trung bình, Volume đột biến
    if atr['trang_thai'] == 'BIẾN_ĐỘNG_CAO' and vol['trang_thai'] == 'DOT_BIEN':
        don_bay_moi -= 3 # Giảm mạnh đòn bẩy
        ly_do = "TIN MẠNH => Biến động & Volume đột biến."

    # 2. SIDEWAY (Thị trường đi ngang, nén)
    # Đặc điểm: ATR thấp, ADX < 20, Bollinger bóp (squeeze)
    elif adx['trang_thai'] == 'SIDEWAY' and bb['trang_thai'] == 'BOP':
        don_bay_moi = min(don_bay, 10) # Giới hạn đòn bẩy thấp (ví dụ max 10x)
        ly_do = "SIDEWAY => ADX thấp + BB bóp. Thị trường tích lũy,"

    # 3. BREAKOUT RÕ (Xác nhận xu hướng)
    # Đặc điểm: Giá phá đỉnh/đáy, Volume tăng, ADX > 25
    elif brk['trang_thai'] != 'KHONG' and adx['trang_thai'] == 'CO_XU_HUONG' and vol['trang_thai'] != 'THAP':
        don_bay_moi = don_bay # Giữ đòn bẩy vừa phải (theo chiến lược gốc)
        ly_do = f"BREAKOUT => Brk {brk['trang_thai']}, Vol ổn định."

    # 4. LOGIC MẶC ĐỊNH (Theo yêu cầu cũ của bạn)
    else:
        if atr['atr_val'] > atr['atr_mean'] * 1.05:
            don_bay_moi -= 1
            ly_do = "ATR > Mean 5%: Giảm nhẹ Leverage."
        elif atr['atr_val'] < atr['atr_mean'] * 0.95:
            don_bay_moi += 1
            ly_do = "ATR < Mean 5%: Tăng nhẹ Leverage."
        else:
            ly_do = "Thị trường ổn định."

    # Đảm bảo đòn bẩy nằm trong khoảng an toàn (tối thiểu 1x, tối đa 50x)
    don_bay_moi = max(1, min(50, don_bay_moi))
    
    if don_bay_moi != don_bay:
        logger.info(
            f"[LEV  ] {symbol:<9}  {'LEV':<2} | "
            f"    {don_bay}x -> {don_bay_moi}x{'':<2}   | "  # Khoảng trắng để đẩy cột Lý do ra sau cho thẳng hàng
            f"R: {ly_do}"
        )

    return don_bay_moi
