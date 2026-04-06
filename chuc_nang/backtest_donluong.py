import sys
import os
import time
import json
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

try:
    from utils.log import logger, set_log_time, reset_log_time
    from utils.doc_cau_hinh import lay_cau_hinh_giao_dich, lay_cau_hinh_ao
    from lay_du_lieu.lay_ohlcv import gop_nen, tai_du_lieu_lich_su, chuan_bi_du_lieu_da_khung
    from chien_luoc.quan_ly_chien_luoc import chien_luoc_vao_lenh, chien_luoc_thoat_lenh
    from chien_luoc.stoploss_takeprofit import tinh_sl_tp_theo_atr
    from chien_luoc.chien_luoc_don_bay import phan_tich_don_bay
    from utils.thoi_gian import lay_timestamp_ms

    from ml.trang_thai_thi_truong_ml.ml_predict import danh_gia_ml
except ImportError as e:
    logger.info(f"❌ Lỗi Import: {e}")
    logger.info("Vui lòng chạy script từ thư mục gốc hoặc đảm bảo cấu trúc thư mục đúng.")
    sys.exit(1)


def chay_backtest(return_data=False, callback=None):
    config_backtest = lay_cau_hinh_ao()
    config_trading = lay_cau_hinh_giao_dich()
    
    VON_BAN_DAU = float(config_backtest.get('so_du_ban_dau',))
    PHI_GD = float(config_backtest.get('phi_giao_dich',))
    SLIPPAGE = float(config_backtest.get('do_truot_gia',))
    START_DATE = config_backtest.get('ngay_bat_dau', '')
    END_DATE = config_backtest.get('ngay_ket_thuc', '')
    
    DON_BAY = int(config_trading.get('don_bay',))
    DS_SYMBOL = config_trading.get('cap_giao_dich', [])
    VON_MOI_LENH = float(config_trading.get('von_moi_lenh_usdt',))
    CAT_LO_PCT = float(config_trading.get('cat_lo_percent',))
    CHOT_LOI_PCT = float(config_trading.get('chot_loi_percent',))

    von_hien_tai = VON_BAN_DAU
    lich_su_lenh = []

    bien_dong_tai_san = [{'time': START_DATE, 'balance': VON_BAN_DAU}]

    print("")
    logger.info(" ╔" + "═"*50 + "╗")
    logger.info(f" ║{'🚀 BẮT ĐẦU BACKTEST 🚀':^48}║")
    logger.info(" ╚" + "═"*50 + "╝")
    logger.info(f"    📅 Thời gian : {START_DATE} -> {END_DATE}")
    logger.info(f"    💰 Vốn gốc   : {VON_BAN_DAU:,.2f}$")
    logger.info(f"    ⚙️ Cài đặt   : Phí {PHI_GD*100}% | Slippage {SLIPPAGE*100}%")
    logger.info("─"*52)
    print("")


    for symbol in DS_SYMBOL:
        logger.info(f"🔍 Đang xử lý cặp: {symbol}")
        
        df_goc = tai_du_lieu_lich_su(symbol, START_DATE, END_DATE)
        if df_goc.empty:
            logger.info(f"⚠️ Không có dữ liệu cho {symbol}, bỏ qua.")
            continue

        vi_the = None

        idx_start = 43200 
        if len(df_goc) < idx_start:
            logger.info("⚠️ Dữ liệu quá ngắn.")
            continue
            
        timestamps = df_goc.index[idx_start:]

        last_price_close = 0
        last_time_str = ""

        # tham số ml đánh giá
        dinh_tai_khoan = von_hien_tai
        
        for current_time in timestamps:

            start_time = lay_timestamp_ms()

            print (f"⏳ {current_time}", end='\r')
            dfs = chuan_bi_du_lieu_da_khung(df_goc, current_time)
            if not dfs: continue
            
            df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d = dfs

            nen_hien_tai = df_1m.iloc[-1]
            gia_close = nen_hien_tai['close']
            gia_high = nen_hien_tai['high']
            gia_low = nen_hien_tai['low']

            last_price_close = gia_close
            str_time = current_time.strftime('%Y-%m-%d %H:%M')
            last_time_str = str_time

            if vi_the:
                side = vi_the['side']
                value = vi_the['value']
                entry = vi_the['entry']
                sl_price = vi_the['sl_price']
                tp_price = vi_the['tp_price']
                amount = vi_the['amount'] 
                don_bay = vi_the['leverage']
                time_open = vi_the['time_open']
                phi_mo_lenh = vi_the['phi_mo']
                chien_luoc = vi_the['chien_luoc']
                
                can_thoat = False
                ly_do_thoat = ""
                gia_khop_thoat = gia_close 

                if side == 'buy':
                    roe_low_pct = ((gia_low - entry) / entry) * don_bay
                    roe_high_pct = ((gia_high - entry) / entry) * don_bay
                else:
                    roe_low_pct = ((entry - gia_low) / entry) * don_bay
                    roe_high_pct = ((entry - gia_high) / entry) * don_bay

                if side == 'buy':
                    if gia_low <= sl_price or roe_low_pct <= -CAT_LO_PCT:
                        can_thoat = True
                        ly_do_thoat = "SL (Hit Price/ROE)"
                        gia_khop_thoat = sl_price if gia_low <= sl_price else gia_low

                    elif gia_high >= tp_price or roe_high_pct >= CHOT_LOI_PCT:
                        can_thoat = True
                        ly_do_thoat = "TP (Hit Price/ROE)"
                        gia_khop_thoat = tp_price if gia_high >= tp_price else gia_high

                else:
                    if gia_high >= sl_price or roe_high_pct <= -CAT_LO_PCT:
                        can_thoat = True
                        ly_do_thoat = "SL (Hit Price/ROE)"
                        gia_khop_thoat = sl_price if gia_high >= sl_price else gia_high

                    elif gia_low <= tp_price or roe_low_pct >= CHOT_LOI_PCT:
                        can_thoat = True
                        ly_do_thoat = "TP (Hit Price/ROE)"
                        gia_khop_thoat = tp_price if gia_low <= tp_price else gia_low

                if not can_thoat:
                    check_thoat, reason = chien_luoc_thoat_lenh(
                        symbol, side, chien_luoc, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d
                    )
                    if check_thoat:
                        can_thoat = True
                        ly_do_thoat = f"SIGNAL ({reason})"
                        gia_khop_thoat = gia_close 

                if can_thoat:
                    if side == 'buy':
                        real_pnl_pct = (gia_khop_thoat - entry) / entry
                    else:
                        real_pnl_pct = (entry - gia_khop_thoat) / entry
                    
                    gia_tri_lenh = value * don_bay
                    loi_nhuan_usdt = gia_tri_lenh * real_pnl_pct
                    phi_dong = gia_tri_lenh * PHI_GD
                    
                    net_profit = loi_nhuan_usdt - phi_dong
                    von_hien_tai += net_profit

                    real_pnl_usd = loi_nhuan_usdt - phi_dong - phi_mo_lenh
                    
                    logger.info(
                        f"[ OUT ] {symbol:<9} {side.upper():<4} | "
                        f"Price: {gia_khop_thoat:>9.2f} | "
                        f"PnL: {real_pnl_usd:>+5.2f}$ ({(real_pnl_usd / vi_the['value']) * 100:>+8.2f}%) | "
                        f"S: {chien_luoc}"
                    )
                    
                    lich_su_lenh.append({
                        'symbol': symbol,
                        'time_open': time_open,
                        'time_close': str_time,
                        'side': side,
                        'entry': entry,
                        'exit': gia_khop_thoat,
                        'leverage': don_bay,
                        'pnl_usd': real_pnl_usd,
                        'pnl_pct': real_pnl_usd/vi_the['value'],
                        'score': vi_the['diem'],
                        'strategy': chien_luoc,
                        'reason': ly_do_thoat,
                    })

                    bien_dong_tai_san.append({
                    'time': str_time,
                    'balance': von_hien_tai
                    })

                    if callback:
                        callback({
                            "trades": lich_su_lenh,
                            "equity_curve": bien_dong_tai_san,
                            "initial_capital": VON_BAN_DAU,
                            "final_capital": von_hien_tai
                        })

                    # Đánh giá hiệu quả ML
                    if von_hien_tai > dinh_tai_khoan:
                        dinh_tai_khoan = von_hien_tai
                    account_drawdown = (von_hien_tai - dinh_tai_khoan) / dinh_tai_khoan * 100
                    danh_gia_ml(vi_the['packet'], (real_pnl_usd / vi_the['value']) * 100, account_drawdown)

                    # Reset vị thế
                    vi_the = None

            if not vi_the:
                tin_hieu, diem, chien_luoc, ly_do, packet = chien_luoc_vao_lenh(
                    symbol, current_time, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d
                )
                
                if tin_hieu:
                    don_bay = phan_tich_don_bay(symbol, DON_BAY, df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d)

                    gia_vao = gia_close * (1 + SLIPPAGE) if tin_hieu == 'buy' else gia_close * (1 - SLIPPAGE)

                    sl_price, tp_price = tinh_sl_tp_theo_atr(gia_vao, tin_hieu, df_15m)
                    
                    gia_tri_lenh = VON_MOI_LENH * don_bay
                    so_luong_coin = gia_tri_lenh / gia_vao
                    phi_mo = gia_tri_lenh * PHI_GD
                    
                    von_hien_tai -= phi_mo
                    
                    vi_the = {
                        'side': tin_hieu,
                        'entry': gia_vao,
                        'amount': so_luong_coin,
                        'value': VON_MOI_LENH,
                        'sl_price': sl_price,
                        'tp_price': tp_price,
                        'time_open': str_time,
                        'leverage': don_bay,
                        'phi_mo': phi_mo,
                        'chien_luoc': chien_luoc,
                        'diem': diem,
                        'ly_do': ly_do,
                        'packet': packet
                    }
                    
                    logger.info(
                        f"[ IN  ] {symbol:<9} {tin_hieu.upper():<4} | "
                        f"Entry: {gia_vao:>9.2f} | "
                        f"Fee: {phi_mo:>6.2f}$ (Sc:{diem:>5}) | "
                        f"S: {chien_luoc}"
                    ) 

            end_time = lay_timestamp_ms()
            thoi_gian_xu_ly_ms = end_time - start_time

            print(f"⏳ {current_time} | Xử lý trong: {thoi_gian_xu_ly_ms} ms", end='\r')
                    
        if vi_the:
            logger.info(f"⚠️ Đóng cưỡng bức lệnh treo {symbol} tại giá cuối cùng: {last_price_close}")
            side = vi_the['side']
            value = vi_the['value']
            entry = vi_the['entry']
            don_bay = vi_the['leverage']
            time_open = vi_the['time_open']
            phi_mo_lenh = vi_the.get('phi_mo', 0)
            
            gia_khop_thoat = last_price_close
            
            if side == 'buy':
                raw_pnl_pct = (gia_khop_thoat - entry) / entry
            else:
                raw_pnl_pct = (entry - gia_khop_thoat) / entry
            
            gia_tri_lenh = value * don_bay
            loi_nhuan_tho = gia_tri_lenh * raw_pnl_pct
            phi_dong = gia_tri_lenh * PHI_GD
            
            balance_change = loi_nhuan_tho - phi_dong
            von_hien_tai += balance_change
            
            real_pnl_usd = loi_nhuan_tho - phi_dong - phi_mo_lenh
            
            lich_su_lenh.append({
                'symbol': symbol,
                'time_open': time_open,
                'time_close': last_time_str,
                'side': side,
                'entry': entry,
                'exit': gia_khop_thoat,
                'pnl_usd': real_pnl_usd,
                'pnl_pct': raw_pnl_pct,
                'reason': "FORCE CLOSE (END)",
                'balance': von_hien_tai
            })
            bien_dong_tai_san.append({'time': last_time_str, 'balance': von_hien_tai})

            if callback:
                callback({
                    "trades": lich_su_lenh,
                    "equity_curve": bien_dong_tai_san,
                    "initial_capital": VON_BAN_DAU,
                    "final_capital": von_hien_tai
                })

    print("")
    logger.info("╔" + "═"*50 + "╗")
    logger.info(f"║{'📊 KẾT QUẢ BACKTEST':^49}║")
    logger.info("╚" + "═"*50 + "╝")
    logger.info(f"Vốn ban đầu : {VON_BAN_DAU:,.2f}$")
    logger.info(f"Vốn cuối cùng: {von_hien_tai:,.2f}$")
    loi_nhuan = von_hien_tai - VON_BAN_DAU
    logger.info(f"Lợi nhuận ròng: {loi_nhuan:,.2f}$ ({(loi_nhuan/VON_BAN_DAU)*100:.2f}%)")
    logger.info(f"Tổng số lệnh  : {len(lich_su_lenh)}")
    
    wins = [x for x in lich_su_lenh if x['pnl_usd'] > 0]
    losses = [x for x in lich_su_lenh if x['pnl_usd'] <= 0]
    logger.info(f"Thắng: {len(wins)} | Thua: {len(losses)}")
    if len(lich_su_lenh) > 0:
        win_rate = len(wins) / len(lich_su_lenh) * 100
        logger.info(f"Tỷ lệ thắng (Winrate): {win_rate:.2f}%")

    if lich_su_lenh:
        folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'du_lieu', 'thong_tin_lenh')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        file_name = f"ket_qua_backtest_{int(time.time())}.csv"
        save_path = os.path.join(folder_path, file_name)
        
        pd.DataFrame(lich_su_lenh).to_csv(save_path, index=False)
        logger.info(f"💾 Đã lưu chi tiết lịch sử lệnh tại:\n   {save_path}")

    if return_data:
        return {
            "initial_capital": VON_BAN_DAU,
            "final_capital": von_hien_tai,
            "trades": lich_su_lenh,
            "equity_curve": bien_dong_tai_san
        }

if __name__ == "__main__":
    chay_backtest()