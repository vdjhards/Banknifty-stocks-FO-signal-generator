from dataclasses import dataclass

BREAKOUT_TIMES = tuple(f'{hour:02d}:{minute:02d}' for hour in range(10, 14) for minute in (0, 15, 30, 45))
BREAKOUT_TIMES = tuple(t for t in BREAKOUT_TIMES if t <= '13:00')
SESSION_TIMES = BREAKOUT_TIMES + ('13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', '15:00', '15:15')
COIL_TIMES = ('09:30', '09:45', '10:00', '10:15')

@dataclass
class Signal:
    action: str
    score: int
    entry: float
    stop: float
    target1: float
    target2: float
    reason: str


def build_signal(df15):
    """Apply the 15-minute opening-range inside-bar rule.

    The signal is emitted only once the entry candle exists, so entry is its
    actual open rather than the unavailable close of the breakout candle.
    """
    if df15.empty:
        return None

    day = df15.index[-1].date()
    session = df15[(df15.index.date == day) & df15.index.strftime('%H:%M').isin(('09:15', *COIL_TIMES, *SESSION_TIMES))]
    candle_one = session[session.index.strftime('%H:%M') == '09:15']
    if candle_one.empty:
        return None
    candle_one = candle_one.iloc[0]
    high, low = float(candle_one.High), float(candle_one.Low)
    if high <= low:
        return None

    for candle_time in COIL_TIMES:
        coil = session[session.index.strftime('%H:%M') == candle_time]
        if coil.empty or float(coil.iloc[0].High) > high or float(coil.iloc[0].Low) < low:
            return None

    for position, candle_time in enumerate(BREAKOUT_TIMES):
        breakout = session[session.index.strftime('%H:%M') == candle_time]
        if breakout.empty:
            continue
        breakout = breakout.iloc[0]
        close = float(breakout.Close)
        if close > high:
            action, stop, target = 'BUY CALL', low, float(breakout.Close) * 1.01
        elif close < low:
            action, stop, target = 'BUY PUT', high, float(breakout.Close) * 0.99
        else:
            continue

        entry_time = SESSION_TIMES[SESSION_TIMES.index(candle_time) + 1]
        entry = session[session.index.strftime('%H:%M') == entry_time]
        if entry.empty:
            return None
        entry_price = float(entry.iloc[0].Open)
        if action == 'BUY CALL':
            target = entry_price * 1.01
        else:
            target = entry_price * 0.99
        return Signal(action, 0, entry_price, stop, target, target, f'15M inside-bar breakout at {candle_time}; entry at {entry_time} open')
    return None
