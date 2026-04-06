""" THỜI GIAN & CHU KỲ (Time / Cycle) ⭐
👉 Khi nào thị trường hay phản ứng?
- Phiên Á – Âu – Mỹ
- Thời điểm ra tin
- Chu kỳ nến
- Session Range
📌 Dùng để:
- Tránh giao dịch lúc nhiễu
- Giảm leverage giờ rủi ro
- Bot futures rất cần """

def pt_kiem_tra_ngay(dt): #chien_luoc_trang_thai_thi_truong
    """Kiểm tra ngày trong tuần (Thứ 2 - Thứ 6)"""
    thu_may = dt.weekday()  # 0: Thứ 2, 6: Chủ Nhật
    hợp_lệ = 0 <= thu_may <= 6
    
    return {
        'gia_tri': thu_may + 2,
        'trang_thai': 'HỢP_LỆ' if hợp_lệ else 'CUỐI_TUẦN'
    }

def pt_kiem_tra_gio(dt): #chien_luoc_trang_thai_thi_truong
    """Kiểm tra khung giờ giao dịch (Tránh giờ giãn spread 5h sáng)"""
    gio = dt.hour
    hợp_lệ = (gio != 5) # False nếu là 5h sáng VN
    
    return {
        'gia_tri': gio,
        'trang_thai': 'HỢP_LỆ' if hợp_lệ else 'GIÃN_SPREAD'
    }