from datetime import datetime, time
from zoneinfo import ZoneInfo
import yfinance as yf
from .config import SYMBOL, MARKET_TZ, MIN_SCORE
from .indicators import add_indicators
from .timesfm_forecaster import forecast_direction
from .strategy import build_signal
from .journal import add
from .telegram import send

def completed(df, minutes):
    df=df.copy(); df.index=df.index.tz_convert(MARKET_TZ) if df.index.tz is not None else df.index.tz_localize('UTC').tz_convert(MARKET_TZ)
    now=datetime.now(ZoneInfo(MARKET_TZ)); cutoff=now.replace(second=0,microsecond=0)
    cutoff=cutoff.replace(minute=(cutoff.minute//minutes)*minutes)
    return df[df.index < cutoff]

def main():
    now=datetime.now(ZoneInfo(MARKET_TZ))
    if now.weekday()>=5 or not (time(9,15)<=now.time()<=time(15,40)): return
    raw=yf.download(SYMBOL, period='5d', interval='5m', auto_adjust=False, progress=False)
    if raw.empty: return
    if hasattr(raw.columns,'levels'): raw.columns=raw.columns.get_level_values(0)
    df5=completed(raw,5)
    if len(df5)<80: return
    df5=add_indicators(df5)
    df15=df5.resample('15min',label='right',closed='right').agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).dropna()
    if len(df15)<100: return
    direction, future, pct=forecast_direction(df15['Close'].tail(1024).values)
    sig=build_signal(df5,direction)
    if not sig: return
    candle=df5.index[-1].isoformat()
    if add(sig,candle):
        send(f"🚨 BANKNIFTY SIGNAL\n\nAction: {sig.action}\nScore: {sig.score}/100\n\nBANKNIFTY: {sig.entry:.2f}\nEntry: {sig.entry:.2f}\nStop Loss: {sig.stop:.2f}\nTarget 1: {sig.target1:.2f}\nTarget 2: {sig.target2:.2f}\n\n15M TimesFM: {direction}\n5M Breakout: CONFIRMED\n\nReason: {sig.reason}\n\n⚠️ PAPER TRADE — score is strategy strength, not win probability.")
if __name__=='__main__': main()
