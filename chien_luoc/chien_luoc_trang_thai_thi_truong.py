from chien_luoc.logic_giao_dich.phan_tich_ky_thuat.chu_ky import pt_kiem_tra_gio, pt_kiem_tra_ngay
from ml.trang_thai_thi_truong_ml.ml_predict import du_doan_trang_thai_ml

#df_1m có 300 nến, df_3m có 100 nến, df_5m có 300 nến, df_15m có 100 nến, df_30m có 300 nến, df_1h có 150 nến, df_4h có 300 nến, df_1d có 50 nến
def phan_tich_trang_thai_thi_truong(symbol, Datetime, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h):

    # 1. Kiểm tra điều kiện thời gian
    kq_ngay = pt_kiem_tra_ngay(Datetime)
    kq_gio = pt_kiem_tra_gio(Datetime)
    
    if not (kq_ngay['trang_thai'] == 'HỢP_LỆ' and kq_gio['trang_thai'] == 'HỢP_LỆ'):
        return False, f"NGHỈ ({kq_ngay['trang_thai']})"

    packet = du_doan_trang_thai_ml(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h)

    return True, packet
