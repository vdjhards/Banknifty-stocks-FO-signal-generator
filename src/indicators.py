import numpy as np
import pandas as pd

def add_indicators(df):
    x = df.copy()
    x['ema20'] = x['Close'].ewm(span=20, adjust=False).mean()
    x['ema50'] = x['Close'].ewm(span=50, adjust=False).mean()
    tp = (x['High'] + x['Low'] + x['Close']) / 3
    x['vwap'] = (tp * x['Volume']).cumsum() / x['Volume'].replace(0, np.nan).cumsum()
    delta = x['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    x['rsi'] = 100 - (100 / (1 + rs))
    tr = pd.concat([(x['High']-x['Low']), (x['High']-x['Close'].shift()).abs(), (x['Low']-x['Close'].shift()).abs()], axis=1).max(axis=1)
    x['atr'] = tr.rolling(14).mean()
    x['vol_ratio'] = x['Volume'] / x['Volume'].rolling(20).mean()
    x['resistance'] = x['High'].rolling(12).max().shift(1)
    x['support'] = x['Low'].rolling(12).min().shift(1)
    return x
