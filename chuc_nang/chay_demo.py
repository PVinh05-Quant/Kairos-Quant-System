import threading
import time
import sys
import os
import signal
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from utils.doc_cau_hinh import lay_cau_hinh_giao_dich, lay_cau_hinh_ao
from utils.ham_tien_ich import chuyen_doi_symbol_chuan, tinh_pnl
from utils.chuyen_doi_don_vi import usdt_sang_so_luong_coin, lam_tron_khoi_luong, mili_giay_sang_phut
from utils.thoi_gian import ngu_an_toan, lay_timestamp_ms
from utils.log import logger
from lay_du_lieu.lay_ohlcv import lay_du_lieu_nen
from lay_du_lieu.lay_marketsnapshot import mo_theo_doi, dong_theo_doi
from chien_luoc.quan_ly_chien_luoc import chien_luoc_vao_lenh, chien_luoc_thoat_lenh

from thuc_thi_lenh.quan_ly_danh_muc import kiem_tra_phan_bo_von
from chien_luoc.stoploss_takeprofit import tinh_sl_tp_theo_atr
from chien_luoc.chien_luoc_don_bay import phan_tich_don_bay
from thuc_thi_lenh import quan_ly_lenh

from ml.trang_thai_thi_truong_ml.ml_predict import danh_gia_ml

CONFIG = lay_cau_hinh_giao_dich()
SAN_CHINH = CONFIG.get('san_giao_dich_chinh', 'binance').lower()
RAW_COINS = CONFIG.get('cap_giao_dich', [])
DON_BAY = int(CONFIG.get('don_bay',))

LIST_COIN = [chuyen_doi_symbol_chuan(SAN_CHINH, coin) for coin in RAW_COINS]

MAX_OPEN_ORDERS = CONFIG.get('max_lenh_cho_phep')

config_demo = lay_cau_hinh_ao()
VON_AO = float(config_demo.get('so_du_ban_dau'))
PHI_GIAO_DICH = float(config_demo.get('phi_giao_dich'))
DO_TRUOT_GIA = float(config_demo.get('do_truot_gia'))

CHUC_NANG = 'demo'
DANG_CHAY = True
lich_su_lenh_ao = []

def luong_quet_thi_truong_demo():
    global VON_AO
    logger.info(f"🎮 [DEMO] Bắt đầu quét thị trường (Vốn: {VON_AO:,.2f}$)...")
    
    while DANG_CHAY:
        so_lenh_dang_mo = len(quan_ly_lenh.lay_danh_sach_symbol_dang_co())
        if not kiem_tra_phan_bo_von(VON_AO, so_lenh_dang_mo, max_lenh_cho_phep=MAX_OPEN_ORDERS):
            logger.info(f"💤 [DEMO] Đã đạt giới hạn {MAX_OPEN_ORDERS} lệnh. Tạm nghỉ quét...")
            ngu_an_toan(10)
            continue

        for symbol in LIST_COIN:
            if quan_ly_lenh.kiem_tra_ton_tai(symbol):
                continue

            try:
                start_time = lay_timestamp_ms()

                df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d = lay_du_lieu_nen(SAN_CHINH, symbol)

                MarketSnapshot = mo_theo_doi(symbol)

                Datetime = datetime.now()
                             
                if df_1m is None: continue

                gia_hien_tai = df_1m['close'].iloc[-1]

                tin_hieu, diem, chien_luoc, ly_do, packet = chien_luoc_vao_lenh(symbol, Datetime, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d, MarketSnapshot)
                if tin_hieu:
                    don_bay = phan_tich_don_bay(symbol, DON_BAY, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d)

                    msg = f"🔔 Tín hiệu {tin_hieu.upper()} cho {symbol} (Điểm: {diem:.2f})"
                    logger.info(msg)
                    
                    gia_tri_lenh = CONFIG['von_moi_lenh_usdt'] * don_bay

                    gia_vao = gia_hien_tai * (1 + DO_TRUOT_GIA) if tin_hieu == 'buy' else gia_hien_tai * (1 - DO_TRUOT_GIA)
                    
                    so_luong_raw = usdt_sang_so_luong_coin(gia_tri_lenh, gia_hien_tai)
                    so_luong = lam_tron_khoi_luong(so_luong_raw, precision_amount=4)

                    phi_mo = gia_tri_lenh * PHI_GIAO_DICH
                    VON_AO -= phi_mo

                    sl_price, tp_price = tinh_sl_tp_theo_atr(
                        gia_vao, 
                        tin_hieu,
                        df_15m
                    )

                    quan_ly_lenh.luu_lenh_moi(CHUC_NANG, symbol, {
                        'side': tin_hieu,
                        'entry_price': gia_vao,
                        'amount': so_luong,
                        'leverage': don_bay,
                        'time': Datetime.strftime('%H:%M:%S'),
                        'sl_price': sl_price,
                        'tp_price': tp_price,
                        'chien_luoc': chien_luoc,
                        'diem': diem,
                        'ly_do_mo': ly_do,
                        'packet_ml': packet
                    })
                    
                    logger.info(
                        f"[ IN  ] {symbol:<9} {tin_hieu.upper():<4} | "
                        f"Entry: {gia_vao:>9.2f} | "
                        f"Fee: {phi_mo:>6.2f}$ (Sc:{diem:>5}) | "
                        f"S: {chien_luoc}"
                    )

                    end_time = lay_timestamp_ms()
                    thoi_gian_xu_ly_ms = end_time - start_time
                    if thoi_gian_xu_ly_ms > 2000:
                        phut_xu_ly = mili_giay_sang_phut(thoi_gian_xu_ly_ms)
                        logger.warning(f"⚠️ Mạng chậm! {symbol} xử lý mất {thoi_gian_xu_ly_ms:.0f}ms")

            except Exception as e:
                logger.error(f"Lỗi quét demo {symbol}: {e}")

            ngu_an_toan(0.2)
                
        ngu_an_toan(5)

def luong_quan_ly_vi_the_demo():
    global VON_AO
    logger.info("🛡️ [DEMO] Bắt đầu quản lý vị thế...")
    
    while DANG_CHAY:
        ds_dang_giu = quan_ly_lenh.lay_danh_sach_symbol_dang_co()
        
        if not ds_dang_giu:
            time.sleep(5)
            continue

        # tham số để tính toán drawdown
        dinh_tai_khoan = VON_AO

        for symbol in ds_dang_giu:
            start_time = lay_timestamp_ms()

            try:
                vt = quan_ly_lenh.lay_thong_tin_lenh(symbol)
                if not vt:
                    continue

                df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d = lay_du_lieu_nen(SAN_CHINH, symbol)

                MarketSnapshot = mo_theo_doi(symbol)

                if df_1m is None: continue

                quan_ly_lenh.data_vi_the_update(symbol, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d)

                gia_hien_tai = df_1m['close'].iloc[-1]
                gia_high = df_1m['high'].iloc[-1]
                gia_low = df_1m['low'].iloc[-1]
                
                sl_price = vt.get('sl_price')
                tp_price = vt.get('tp_price')
                chien_luoc = vt.get('chien_luoc')

                pnl_usdt, pnl_percent = tinh_pnl(vt['entry_price'], gia_hien_tai, vt['side'], vt['amount'])
                roe_percent = pnl_percent * vt['leverage']

                packet_ml = vt.get('packet_ml') # Dữ liệu ML khi mở lệnh

                can_thoat = False
                ly_do = ""
                gia_dong_du_kien = gia_hien_tai

                if sl_price and tp_price:
                    if vt['side'] == 'buy':
                        if gia_high >= tp_price:
                            can_thoat = True
                            ly_do = f"Chạm giá TP ({gia_high} >= {tp_price})"
                            gia_dong_du_kien = tp_price
                        elif gia_low <= sl_price:
                            can_thoat = True
                            ly_do = f"Chạm giá SL ({gia_low} <= {sl_price})"
                            gia_dong_du_kien = sl_price
                    else:
                        if gia_low <= tp_price:
                             can_thoat = True
                             ly_do = f"Chạm giá TP ({gia_low} <= {tp_price})"
                             gia_dong_du_kien = sl_price
                        elif gia_high >= sl_price:
                             can_thoat = True
                             ly_do = f"Chạm giá SL ({gia_high} >= {sl_price})"
                             gia_dong_du_kien = tp_price

                if not can_thoat:
                    if roe_percent >= CONFIG['chot_loi_percent']:
                        can_thoat = True
                        ly_do = f"TP Hit % (Đạt {roe_percent*100:.2f}%)"
                    elif roe_percent <= -CONFIG['cat_lo_percent']:
                        can_thoat = True
                        ly_do = f"SL Hit % (Âm {roe_percent*100:.2f}%)"
                
                if not can_thoat:
                    check_thoat_chien_luoc, ly_do_cl = chien_luoc_thoat_lenh(
                        symbol, vt['side'], chien_luoc, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d, MarketSnapshot
                    )
                    if check_thoat_chien_luoc:
                        can_thoat = True
                        ly_do = f"Tín hiệu đảo chiều ({ly_do_cl})"

                if can_thoat:
                    
                    gia_dong_thuc = gia_dong_du_kien * (1 - DO_TRUOT_GIA) if vt['side'] == 'buy' else gia_dong_du_kien * (1 + DO_TRUOT_GIA)
                    
                    real_pnl_usdt, real_pnl_percent = tinh_pnl(vt['entry_price'], gia_dong_thuc, vt['side'], vt['amount'])
                    phi_dong = abs(gia_dong_thuc * vt['amount']) * PHI_GIAO_DICH
                    
                    net_profit = real_pnl_usdt - phi_dong
                    VON_AO += net_profit
                                    
                    logger.info(f"🔴 [DEMO ĐÓNG] {symbol} | Lý do: {ly_do} | Giá: {gia_dong_thuc:,.2f} | PnL: {net_profit:+.2f}$")
                    
                    lich_su = {
                        'day': datetime.now().strftime('%Y-%m-%d'),
                        'symbol': symbol,
                        'side': vt['side'],
                        'entry_price': vt['entry_price'],
                        'exit_price': gia_dong_thuc,
                        'open_time': vt['time'],
                        'close_time': datetime.now().strftime('%H:%M:%S'),
                        'pnl': net_profit,
                        'score':vt['diem'],
                        'strategy': chien_luoc,
                        'reason': ly_do
                    }

                    lich_su_lenh_ao.append(lich_su)

                    quan_ly_lenh.lich_su_lenh(CHUC_NANG, lich_su)
                    
                    quan_ly_lenh.xoa_lenh(CHUC_NANG, symbol)

                    # Đánh giá hiệu quả ML
                    if VON_AO > dinh_tai_khoan:
                        dinh_tai_khoan = VON_AO
                    account_drawdown = (VON_AO - dinh_tai_khoan) / dinh_tai_khoan * 100
                    danh_gia_ml(packet_ml, real_pnl_percent * 100, account_drawdown)

                end = lay_timestamp_ms()
                thoi_gian_xu_ly_ms = end - start_time
                if thoi_gian_xu_ly_ms > 2000:
                    logger.warning(f"⚠️ [DEMO MANAGER] Xử lý chậm {symbol}: {thoi_gian_xu_ly_ms:.0f}ms")                

                time.sleep(0.2)

            except Exception as e:
                logger.error(f"Lỗi quản lý demo {symbol}: {e}")
        
        time.sleep(5)


def chay_demo():
    print("")
    logger.info(" ╔" + "═"*50 + "╗")
    logger.info(f" ║{'🚀 KHỞI ĐỘNG PAPER TRADING (DEMO)':^49}║")
    logger.info(" ╚" + "═"*50 + "╝")
    logger.info(f" {'💰 Vốn giả lập':<20}: {VON_AO:>15,.2f}$")
    logger.info(f" {'🏦 Sàn dữ liệu':<20}: {SAN_CHINH.upper():>15}")
    logger.info(f" {'📦 Max Orders':<20}: {MAX_OPEN_ORDERS:>15}")
    quan_ly_lenh.load_trang_thai(CHUC_NANG)
    logger.info("─"*52)
    print("")

    t1 = threading.Thread(target=luong_quet_thi_truong_demo, name="Demo-Scanner")
    t2 = threading.Thread(target=luong_quan_ly_vi_the_demo, name="Demo-Manager")

    t1.daemon = True
    t2.daemon = True

    t1.start()
    t2.start()

if __name__ == "__main__":
    chay_demo()