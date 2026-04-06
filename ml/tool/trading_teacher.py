import ta
import numpy as np
import pandas as pd


def trang_thai_thi_truong_ky_thuat(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h):

    # ==============================
    # 1️⃣ Persistence Memory
    # ==============================
    if not hasattr(trang_thai_thi_truong_ky_thuat, "last_state"):
        trang_thai_thi_truong_ky_thuat.last_state = 0
        trang_thai_thi_truong_ky_thuat.change_count = 0

    # ==============================
    # 2️⃣ Feature Engine
    # ==============================
    def _calc_features(df_in):
        if df_in is None or len(df_in) < 120:
            return None, None

        df = df_in.copy().reset_index(drop=True)

        try:
            # --- Volatility ---
            atr = ta.volatility.AverageTrueRange(
                df['high'], df['low'], df['close'], window=14
            ).average_true_range()

            df['atr_n'] = atr / (df['close'] + 1e-8)
            df['vol_cluster'] = df['atr_n'].rolling(20).std()

            # --- Trend ---
            df['ema_50'] = ta.trend.EMAIndicator(df['close'], 50).ema_indicator()
            df['ema_slope'] = df['ema_50'].diff(5) / (df['ema_50'].shift(5) + 1e-8)

            df['adx'] = ta.trend.ADXIndicator(
                df['high'], df['low'], df['close'], window=14
            ).adx()

            df['trendiness'] = abs(df['ema_slope']) / (df['atr_n'] + 1e-8)

            # --- Momentum ---
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], 14).rsi()

            # --- Squeeze ---
            bb = ta.volatility.BollingerBands(df['close'], 20)
            kc = ta.volatility.KeltnerChannel(df['high'], df['low'], df['close'], 20)

            df['is_sqz'] = (
                (bb.bollinger_hband() < kc.keltner_channel_hband()) &
                (bb.bollinger_lband() > kc.keltner_channel_lband())
            )

            # --- Rolling VWAP ---
            window = 100
            df['vwap'] = (
                (df['close'] * df['volume']).rolling(window).sum() /
                (df['volume'].rolling(window).sum() + 1e-8)
            )

            # --- Microstructure ---
            df['body_r'] = abs(df['close'] - df['open']) / (
                (df['high'] - df['low']) + 1e-6
            )
            df['spread_r'] = (df['high'] - df['low']) / (df['close'] + 1e-8)

            last = df.iloc[-1].fillna(0)

            return last, df

        except Exception:
            return None, None

    # ==============================
    # 3️⃣ Extract MTF Features
    # ==============================

    c1h, df1h = _calc_features(df_1h)
    c30m, df30m = _calc_features(df_30m)
    c15m, df15m = _calc_features(df_15m)
    c5m, df5m = _calc_features(df_5m)
    c3m, df3m = _calc_features(df_3m)
    c1m, df1m = _calc_features(df_1m)

    if c1h is None or c1m is None:
        return 0, 0.0

    # ==============================
    # 4️⃣ Scoring Engine
    # ==============================

    scores = {k: 0.0 for k in range(6)}

    # -------- STATE 1: TREND --------
    if c30m is not None and c15m is not None:
        if abs(c1h['ema_slope']) > 0.01 and abs(c30m['ema_slope']) > 0.01:
            if np.sign(c1h['ema_slope']) == np.sign(c30m['ema_slope']):
                scores[1] += 50

        if c15m['adx'] > 25 and c30m['adx'] > 20:
            scores[1] += 30

        if 40 < c15m['rsi'] < 60:
            scores[1] += 20

    # -------- STATE 2: MEAN REVERSION --------
    if c30m is not None and c15m is not None:
        dist_vwap_15 = abs(c15m['close'] - c15m['vwap']) / (
            (c15m['atr_n'] * c15m['close']) + 1e-8
        )
        dist_vwap_30 = abs(c30m['close'] - c30m['vwap']) / (
            (c30m['atr_n'] * c30m['close']) + 1e-8
        )

        if c15m['adx'] < 20 and c30m['adx'] < 22:
            scores[2] += 30
        if c15m['rsi'] > 75 or c15m['rsi'] < 25:
            scores[2] += 40
        if dist_vwap_15 > 1.5 and dist_vwap_30 > 1.2:
            scores[2] += 30

    # -------- STATE 3: SQUEEZE --------
    if c30m is not None and c15m is not None:
        if c15m['is_sqz']:
            scores[3] += 60
        if c30m['is_sqz']:
            scores[3] += 30
        if c15m['atr_n'] < 0.003:
            scores[3] += 10

    # -------- STATE 4: BREAKOUT --------
    if df5m is not None and len(df5m) > 20:
        recent_high = df5m['high'].iloc[-10:-1].max()
        recent_low = df5m['low'].iloc[-10:-1].min()

        if df5m['close'].iloc[-1] > recent_high or \
           df5m['close'].iloc[-1] < recent_low:
            scores[4] += 40

        if df1m is not None and df3m is not None:
            vol_spike_1m = df1m['volume'].iloc[-1] > \
                df1m['volume'].rolling(20).mean().iloc[-1] * 2.5

            vol_spike_3m = df3m['volume'].iloc[-1] > \
                df3m['volume'].rolling(20).mean().iloc[-1] * 2.0

            if vol_spike_1m and vol_spike_3m:
                scores[4] += 40

        if c5m is not None and c5m['body_r'] > 0.7:
            scores[4] += 20

    # -------- STATE 5: SCALPING --------
    if c15m is not None and c1m is not None:
        if c15m['atr_n'] > 0.01:
            scores[5] += 40
        if c1m['spread_r'] > 0.002:
            scores[5] += 30
        if c5m is not None and c5m['adx'] < 20:
            scores[5] += 30

    # -------- STATE 0: NOISE --------
    if df15m is not None and df30m is not None:
        vol_low_15 = df15m['volume'].iloc[-1] < \
            df15m['volume'].rolling(20).mean().iloc[-1] * 0.3

        vol_low_30 = df30m['volume'].iloc[-1] < \
            df30m['volume'].rolling(20).mean().iloc[-1] * 0.3

        if vol_low_15 and vol_low_30:
            scores[0] += 100

    # ==============================
    # 5️⃣ Softmax Probability
    # ==============================

    max_s = max(scores.values())
    exps = {k: np.exp(v - max_s) for k, v in scores.items()}
    total = sum(exps.values())

    probs = {k: exps[k] / total for k in exps}

    raw_state = max(probs, key=probs.get)
    confidence = probs[raw_state]

    # ==============================
    # 6️⃣ Anti-Flicker
    # ==============================

    if raw_state != trang_thai_thi_truong_ky_thuat.last_state:
        trang_thai_thi_truong_ky_thuat.change_count += 1
    else:
        trang_thai_thi_truong_ky_thuat.change_count = 0

    if trang_thai_thi_truong_ky_thuat.change_count >= 3:
        trang_thai_thi_truong_ky_thuat.last_state = raw_state
        trang_thai_thi_truong_ky_thuat.change_count = 0

    return trang_thai_thi_truong_ky_thuat.last_state, float(confidence)
