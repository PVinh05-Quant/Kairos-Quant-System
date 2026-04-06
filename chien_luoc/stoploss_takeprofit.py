from chien_luoc.logic_giao_dich.phan_tich_ky_thuat.bien_dong import pt_atr

def tinh_sl_tp_theo_atr(gia_vao, side, df):
    ket_qua = pt_atr(df)
    atr = ket_qua['atr_val']
    atr_mean = ket_qua['atr_mean']

    if atr is None or atr <= 0:
        return None, None

    if atr_mean is None or atr_mean <= 0:
        vol_ratio = 1.0
    else:
        vol_ratio = atr / atr_mean

    # ===== BASE CONFIG =====
    
    #| Kiểu trade | base_sl       | rr        | Ghi chú
    #| ---------- | ------------- | --------- | -------------------------
    #| Scalping   | 1.5 – 2.0     | 1.5       | Giá sai là cắt liền
    #| Intraday   | 2.0 – 2.5     | 2.0       | Rung được chút, đi đúng là giữ
    #| Swing      | 3.0 – 4.0     | 2.5 – 3.0 | Rung mạnh cũng kệ, miễn trend còn 

    base_sl = 2.7          # base_sl càng LỚN → khoảng SL & TP càng RỘNG
    rr = 2.0               # Risk : Reward

    he_so_sl = base_sl / vol_ratio

    he_so_sl = max(1.0, min(he_so_sl, 6.0))
    he_so_tp = he_so_sl * rr

    if side == 'buy':
        sl = gia_vao - (atr * he_so_sl)
        tp = gia_vao + (atr * he_so_tp)
    else:  # sell
        sl = gia_vao + (atr * he_so_sl)
        tp = gia_vao - (atr * he_so_tp)

    return sl, tp
