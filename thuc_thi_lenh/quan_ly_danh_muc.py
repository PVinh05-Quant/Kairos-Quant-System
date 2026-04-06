from utils.log import logger

def kiem_tra_phan_bo_von(tong_von, so_lenh_dang_mo, max_lenh_cho_phep=5):
    """
    Kiểm tra xem có được phép mở thêm lệnh mới không dựa trên số lượng lệnh.
    """
    if so_lenh_dang_mo >= max_lenh_cho_phep:
        logger.warning(f"⛔ Đạt giới hạn số lệnh tối đa ({max_lenh_cho_phep}). Không mở thêm.")
        return False
    return True

def tinh_ty_trong_von(tong_von, so_luong_coin_muon_trade):
    """
    Chia vốn đều cho các coin trong danh sách theo dõi.
    """
    if so_luong_coin_muon_trade == 0: return 0
    von_moi_coin = tong_von / so_luong_coin_muon_trade
    return von_moi_coin

def kiem_tra_rui_ro_danh_muc(danh_sach_vi_the, max_rui_ro_tong=0.1):
    """
    Kiểm tra tổng rủi ro của danh mục.
    Ví dụ: Nếu tổng rủi ro (tổng tiền có thể mất khi chạm SL) > 10% vốn -> Cảnh báo.
    danh_sach_vi_the: list các dict {'entry': 50000, 'sl': 49000, 'amount': 0.1}
    """
    tong_rui_ro = 0
    for vt in danh_sach_vi_the:
        tien_mat_neu_sl = abs(vt['entry'] - vt['sl']) * vt['amount']
        tong_rui_ro += tien_mat_neu_sl
        
    return tong_rui_ro