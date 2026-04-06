def usdt_sang_so_luong_coin(so_tien_usdt, gia_coin):
    if gia_coin == 0: return 0
    return so_tien_usdt / gia_coin

def mili_giay_sang_phut(ms):
    return ms / (1000 * 60)

def lam_tron_khoi_luong(amount, precision_amount):
    return round(amount, precision_amount)