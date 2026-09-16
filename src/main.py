from datetime import datetime, time
from zoneinfo import ZoneInfo
import yfinance as yf
from .config import SYMBOL, MARKET_TZ
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
    df15=df5.resample('15min',label='left',closed='left').agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).dropna()
    df15=completed(df15,15)
    sig=build_signal(df15)
    if not sig: return
    candle=f'{df15.index[-1].date().isoformat()}|{sig.reason}'
    if add(sig,candle):
        send(f"🚨 BANKNIFTY SIGNAL\n\nAction: {sig.action}\n\nEntry: {sig.entry:.2f}\nStop Loss: {sig.stop:.2f}\nTarget: {sig.target1:.2f}\n\nReason: {sig.reason}\n\n⚠️ PAPER TRADE — 15M inside-bar lab strategy.")
if __name__=='__main__': main()
