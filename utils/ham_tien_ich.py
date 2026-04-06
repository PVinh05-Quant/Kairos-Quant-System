import pandas as pd

def chuyen_doi_symbol_chuan(san, symbol):

    if not symbol: return symbol
   
    symbol = symbol.upper().strip()
    san = san.lower().strip() if san else 'binance'

    if '/' in symbol:
        return symbol

    if san == 'okx':
        clean_symbol = symbol.replace('-SWAP', '').replace('-', '/')
        return clean_symbol

    quote_currencies = ['USDT', 'USDC', 'BUSD', 'TUSD', 'DAI', 'BTC', 'ETH', 'BNB']
    
    for quote in quote_currencies:
        if symbol.endswith(quote):
            base = symbol[:-len(quote)]
            return f"{base}/{quote}"
    return f"{symbol}/USDT"

def tinh_pnl(entry, current_price, side, amount):
    if side == 'buy':
        pnl_usdt = (current_price - entry) * amount
        pnl_percent = (current_price - entry) / entry
    else:
        pnl_usdt = (entry - current_price) * amount
        pnl_percent = (entry - current_price) / entry
    return pnl_usdt, pnl_percent

def gop_va_dong_bo_data(dfs_dict):
    def chuẩn_hóa_df(df, name):
        # 1. Xóa cột không tên (Unnamed) - Tránh rác từ file CSV cũ
        df = df.loc[:, ~df.columns.str.contains('^unnamed', case=False)]
        
        # 2. Xóa cột trống
        if "" in df.columns:
            df = df.drop(columns=[""])

        # Chuẩn hóa tên cột về chữ thường
        df.columns = [col.strip().lower() for col in df.columns]
        
        # 3. Đảm bảo timestamp là một cột để có thể merge_asof
        if 'timestamp' not in df.columns:
            if df.index.name and df.index.name.lower() == 'timestamp':
                df = df.reset_index()
            else:
                raise KeyError(f"Không tìm thấy cột 'timestamp' trong khung {name}.")

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Sắp xếp để merge_asof không lỗi
        return df.sort_values('timestamp').reset_index(drop=True)

    # Lấy khung 1m làm gốc
    if '1m' not in dfs_dict:
        return None
        
    main_df = chuẩn_hóa_df(dfs_dict['1m'].copy(), '1m')

    for tf, df in dfs_dict.items():
        if tf == '1m': continue
        
        df_tf = chuẩn_hóa_df(df.copy(), tf)
        
        # Chỉ lấy timestamp và các chỉ báo (không lấy OHLC khung lớn)
        cols_to_exclude = ['open', 'high', 'low', 'close', 'volume']
        cols_to_use = [col for col in df_tf.columns if col not in cols_to_exclude or col == 'timestamp']
        
        main_df = pd.merge_asof(
            main_df, 
            df_tf[cols_to_use],
            on='timestamp',
            direction='backward',
            suffixes=('', f'_{tf}') # Thêm hậu tố để phân biệt RSI_5m, RSI_15m...
        )
    
    # 4. BƯỚC QUAN TRỌNG NHẤT: Đưa timestamp làm Index
    # Việc này sẽ thay thế hoàn toàn cột số 0, 1, 2...
    main_df.set_index('timestamp', inplace=True)
    
    # Xóa các cột rác phát sinh (nếu có)
    if 'index' in main_df.columns:
        main_df.drop(columns=['index'], inplace=True)
        
    return main_df