from utils.log import logger
from chien_luoc.logic_giao_dich.chien_luoc_breakout import phan_tich_breakout, thoat_breakout

from chien_luoc.chien_luoc_trang_thai_thi_truong import phan_tich_trang_thai_thi_truong


#df_1m có 300 nến, df_3m có 100 nến, df_5m có 300 nến, df_15m có 100 nến, df_30m có 300 nến, df_1h có 150 nến, df_4h có 300 nến, df_1d có 50 nến
def chien_luoc_vao_lenh(symbol, Datetime, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d, MarketSnapshot = None):

    cho_phep, packet = phan_tich_trang_thai_thi_truong(symbol, Datetime, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h)

    if not cho_phep:
        return None, 0, None, "Filter: Cấm trade", None

    if packet is None:
        return None, 0, None, "AI: Không đủ dữ liệu / Lỗi Model", None

    chien_luoc = packet['state_name']

    tin_hieu, diem, ly_do = None, 0, []

    if chien_luoc == "Breakout":
        tin_hieu, diem, ly_do = phan_tich_breakout(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d, MarketSnapshot)
        if tin_hieu and abs(diem) >= 20:
            return tin_hieu, diem, chien_luoc, ly_do, packet

    return None, 0, None, None, None

#df_1m có 300 nến, df_3m có 100 nến, df_5m có 300 nến, df_15m có 100 nến, df_30m có 300 nến, df_1h có 150 nến, df_4h có 300 nến, df_1d có 50 nến
def chien_luoc_thoat_lenh(symbol, vi_the_hien_tai, chien_luoc, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d, MarketSnapshot = None):

    vi_the = vi_the_hien_tai.lower()
    THRESHOLD_EXIT = 0

    if chien_luoc == "Breakout":
        th_breakout, diem_breakout, ly_do_breakout= thoat_breakout(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d, MarketSnapshot)
        if vi_the == 'buy':
            if th_breakout == 'sell' and abs(diem_breakout) >= THRESHOLD_EXIT:
                return True, ly_do_breakout
        elif vi_the == 'sell':
            if th_breakout == 'buy' and abs(diem_breakout) >= THRESHOLD_EXIT:
                return True, ly_do_breakout

    return False, "Giữ lệnh"