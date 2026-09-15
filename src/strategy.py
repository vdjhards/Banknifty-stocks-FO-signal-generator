from dataclasses import dataclass

@dataclass
class Signal:
    action: str
    score: int
    entry: float
    stop: float
    target1: float
    target2: float
    reason: str


def build_signal(df5, tfm_direction):
    r = df5.iloc[-1]
    if any(r.get(k) is None for k in ['atr','resistance','support','ema20','ema50','vwap','rsi','vol_ratio']):
        return None
    close, atr = float(r.Close), float(r.atr)
    bullish = close > float(r.resistance) and tfm_direction == 'BULLISH'
    bearish = close < float(r.support) and tfm_direction == 'BEARISH'
    if not (bullish or bearish):
        return None
    score = 30
    score += 25
    score += 10 if float(r.vol_ratio) >= 1.2 else 0
    score += 10 if ((close > r.ema20 > r.ema50) if bullish else (close < r.ema20 < r.ema50)) else 0
    score += 10 if ((close > r.vwap) if bullish else (close < r.vwap)) else 0
    score += 5 if ((55 <= r.rsi <= 75) if bullish else (25 <= r.rsi <= 45)) else 0
    if score < 75:
        return None
    if bullish:
        return Signal('BUY CALL', score, close, close-1.2*atr, close+1.8*atr, close+2.8*atr, '15M TimesFM bullish + 5M resistance breakout')
    return Signal('BUY PUT', score, close, close+1.2*atr, close-1.8*atr, close-2.8*atr, '15M TimesFM bearish + 5M support breakdown')
