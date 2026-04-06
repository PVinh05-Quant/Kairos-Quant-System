import pandas as pd
from thuc_thi_lenh.bo_may_thuc_thi import quan_ly_san
from utils.log import logger
import ccxt
import sys
import time
from datetime import datetime, timedelta

def gop_nen_bt(df, khung_time):
    if df is None or df.empty:
        return None
    
    logic = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }
    try:
        df_resampled = df.resample(khung_time).apply(logic)
        df_resampled.dropna(inplace=True) 
        return df_resampled
    except Exception as e:
        logger.error(f"Lỗi gộp nến {khung_time}: {e}")
        return None

def gop_nen(df, timeframe_dich): 
    if df is None or df.empty: return None
    rule = timeframe_dich.replace('m', 'min').replace('H', 'h') 
    agg_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }
    try:
        df_res = df.resample(rule, on='timestamp', label='left', closed='left', origin='start_day').agg(agg_dict)
        df_res = df_res.dropna().reset_index()    
        return df_res if len(df_res) >= 25 else None
    except Exception as e:
        logger.error(f"Lỗi gộp nến {timeframe_dich}: {e}")
        return None

def chuan_bi_du_lieu_da_khung(df_goc, current_time, limit_lookback=43200):
    MAX_OUTPUT = 300
    df_den_hien_tai = df_goc[df_goc.index <= current_time]
    
    if df_den_hien_tai.empty:
        return None
    if len(df_den_hien_tai) > limit_lookback:
        df_working = df_den_hien_tai.iloc[-limit_lookback:].copy()
    else:
        df_working = df_den_hien_tai.copy()

    df_1m = df_working
    df_3m = gop_nen_bt(df_working, '3min')
    df_5m = gop_nen_bt(df_working, '5min')
    df_15m = gop_nen_bt(df_working, '15min')
    df_30m = gop_nen_bt(df_working, '30min')
    df_1h = gop_nen_bt(df_working, '1h')
    df_4h = gop_nen_bt(df_working, '4h')
    df_1d = gop_nen_bt(df_working, '1d')
    
    return [df_1m.tail(MAX_OUTPUT), df_3m.tail(MAX_OUTPUT), df_5m.tail(MAX_OUTPUT), df_15m.tail(MAX_OUTPUT), df_30m.tail(MAX_OUTPUT), df_1h.tail(MAX_OUTPUT), df_4h.tail(MAX_OUTPUT), df_1d.tail(MAX_OUTPUT)]

def chuan_bi_du_lieu_da_khung_vectorized(df_goc):

    df_1m = df_goc
    df_3m = gop_nen_bt(df_goc, '3min')
    df_5m = gop_nen_bt(df_goc, '5min')
    df_15m = gop_nen_bt(df_goc, '15min')
    df_30m = gop_nen_bt(df_goc, '30min')
    df_1h = gop_nen_bt(df_goc, '1h')
    df_4h = gop_nen_bt(df_goc, '4h')
    df_1d = gop_nen_bt(df_goc, '1d')
    
    return [df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d]
    
def fetch_raw(exchange, symbol, timeframe, limit=1000):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)        
        return df
    except Exception as e:
        logger.error(f"Lỗi fetch {symbol} {timeframe}: {e}")
        return None

def lay_du_lieu_nen(ten_san, symbol): #df_1m có 300 nến, df_3m có 100 nến, df_5m có 300 nến, df_15m có 100 nến, df_30m có 300 nến, df_1h có 150 nến, df_4h có 300 nến, df_1d có 50 nến
    exchange = quan_ly_san.lay_san(ten_san)
    df_1m = df_3m = df_5m = df_15m = df_30m = df_1h = df_4h = df_1d = None
    if not exchange:
        return df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d

    df_1m = fetch_raw(exchange, symbol, '1m', limit=300)
    if df_1m is not None:
        df_3m = gop_nen(df_1m, '3m') #100

    df_5m = fetch_raw(exchange, symbol, '5m', limit=300)
    if df_5m is not None:
        df_15m = gop_nen(df_5m, '15m') #100

    df_30m = fetch_raw(exchange, symbol, '30m', limit=300)
    if df_30m is not None:
        df_1h = gop_nen(df_30m, '1h') #150

    df_4h = fetch_raw(exchange, symbol, '4h', limit=300)
    if df_4h is not None:
        df_1d = gop_nen(df_4h, '1d') #50

    return df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d

def tai_du_lieu_lich_su(symbol, start_str, end_str):
    try:
        start_obj = datetime.strptime(start_str, '%Y-%m-%d')
        since_obj = start_obj - timedelta(days=30)
        since_str = since_obj.strftime('%Y-%m-%d')       
        logger.info(f"⬇️ Đang tải dữ liệu {symbol} từ {since_str} (Buffer 30 ngày) đến {end_str}...")
    except ValueError:
        logger.error(f"❌ Định dạng ngày {start_str} không hợp lệ. Vui lòng dùng YYYY-MM-DD")
        return pd.DataFrame()
    exchange = ccxt.binance() 

    try:
        since = exchange.parse8601(f"{since_str} 00:00:00")
        end_ts = exchange.parse8601(f"{end_str} 23:59:59")
    except Exception as e:
        logger.error(f"Lỗi parse ngày tháng: {e}")
        return pd.DataFrame()
    all_ohlcv = []
    limit = 1000

    while since < end_ts:
        try:
            data = exchange.fetch_ohlcv(symbol, '1m', since=since, limit=limit)
            if not data:
                break         
            last_timestamp = data[-1][0]
            if last_timestamp == since:
                break             
            since = last_timestamp + 60_000
            all_ohlcv.extend(data)           
            time.sleep(0.1)           
        except Exception as e:
            logger.info(f"❌ Lỗi tải data: {e}")
            time.sleep(2)  
    if not all_ohlcv:
        return pd.DataFrame()
    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[~df.index.duplicated(keep='first')]  
    mask = (df.index >= since_obj) & (df.index <= pd.to_datetime(f"{end_str} 23:59:59"))
    df = df.loc[mask]
    #df = df.reset_index()  
    return df
