import ta
import numpy as np
import pandas as pd


def feature_dataset(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h):

    EMA_LEN = 50
    ADX_LEN = 14
    RSI_LEN = 14
    BB_LEN = 20
    VOL_MA_LEN = 20
    ATR_LEN = 14

    data_dict = {
        '1m': df_1m, '3m': df_3m, '5m': df_5m,
        '15m': df_15m, '30m': df_30m, '1h': df_1h
    }

    feature_row = {}

    for tf, df in data_dict.items():

        if df is None or len(df) < 120:
            continue

        df = df.copy().reset_index(drop=True)
        suffix = tf.upper()

        try:

            # ================= TREND =================
            ema = ta.trend.EMAIndicator(df['close'], EMA_LEN).ema_indicator()
            adx = ta.trend.ADXIndicator(df['high'], df['low'], df['close'], ADX_LEN)

            # ================= MOMENTUM =================
            rsi = ta.momentum.RSIIndicator(df['close'], RSI_LEN).rsi()

            macd = ta.trend.MACD(df['close'])
            
            # ================= VOLATILITY =================
            atr = ta.volatility.AverageTrueRange(
                df['high'], df['low'], df['close'], ATR_LEN
            ).average_true_range()

            bb = ta.volatility.BollingerBands(df['close'], BB_LEN)

            # ================= VOLUME =================
            vol_sma = ta.trend.SMAIndicator(df['volume'], VOL_MA_LEN).sma_indicator()

            # ================= LẤY DÒNG CUỐI =================
            i = -1

            feature_row[f'D_{suffix}'] = (df['close'].iloc[i] - ema.iloc[i]) / (ema.iloc[i] + 1e-9)
            feature_row[f'S_{suffix}'] = (ema.iloc[i] - ema.iloc[i-5]) / (ema.iloc[i-5] + 1e-9)

            feature_row[f'ADX_{suffix}'] = adx.adx().iloc[i]
            feature_row[f'DIplus_{suffix}'] = adx.adx_pos().iloc[i]
            feature_row[f'DIminus_{suffix}'] = adx.adx_neg().iloc[i]

            feature_row[f'RSI_{suffix}'] = rsi.iloc[i]

            feature_row[f'MACD_{suffix}'] = macd.macd().iloc[i]
            feature_row[f'MACDdiff_{suffix}'] = macd.macd_diff().iloc[i]

            feature_row[f'ATRn_{suffix}'] = atr.iloc[i] / (df['close'].iloc[i] + 1e-9)

            feature_row[f'BBwidth_{suffix}'] = (
                bb.bollinger_hband().iloc[i] -
                bb.bollinger_lband().iloc[i]
            ) / (bb.bollinger_mavg().iloc[i] + 1e-9)

            feature_row[f'VOLrel_{suffix}'] = df['volume'].iloc[i] / (vol_sma.iloc[i] + 1e-9)

            feature_row[f'BODY_{suffix}'] = abs(
                df['close'].iloc[i] - df['open'].iloc[i]
            ) / ((df['high'].iloc[i] - df['low'].iloc[i]) + 1e-9)

        except Exception:
            continue

    # Nếu không đủ feature → return None
    if len(feature_row) == 0:
        return None

    feature_df = pd.DataFrame([feature_row])

    feature_df = feature_df.replace([np.inf, -np.inf], 0)
    feature_df = feature_df.fillna(0)

    return feature_df
