from collections import Counter
from .journal import load

def report():
    items=load(); today=__import__('datetime').datetime.now(__import__('zoneinfo').ZoneInfo('Asia/Kolkata')).date().isoformat(); trades=[x for x in items if x['time'].startswith(today)]
    wins=sum(x.get('status')=='WIN' for x in trades); losses=sum(x.get('status')=='LOSS' for x in trades); open_=len(trades)-wins-losses
    wr=(wins/(wins+losses)*100) if wins+losses else 0
    lines=[f'📊 BANKNIFTY DAILY REPORT\nDate: {today}',f'\nSignals Generated: {len(trades)}',f'✅ Wins: {wins}',f'❌ Losses: {losses}',f'⏳ Unresolved: {open_}',f'Win Rate: {wr:.1f}%']
    for i,t in enumerate(trades,1): lines.append(f"\nTRADE #{i}\n{t['action']} | Entry {t['entry']:.2f} | SL {t['stop']:.2f} | T1 {t['target1']:.2f} | T2 {t['target2']:.2f}\nStatus: {t.get('status','OPEN')}")
    return '\n'.join(lines)
