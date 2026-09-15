import json
from datetime import datetime
from .config import JOURNAL

def load():
    if not JOURNAL.exists(): return []
    try: return json.loads(JOURNAL.read_text())
    except Exception: return []

def save(items):
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(items, indent=2))

def add(signal, candle_time):
    items=load()
    key=f"{candle_time}|{signal.action}"
    if any(x.get('key')==key for x in items): return False
    items.append({'key':key,'time':candle_time,'action':signal.action,'score':signal.score,'entry':signal.entry,'stop':signal.stop,'target1':signal.target1,'target2':signal.target2,'status':'OPEN'})
    save(items); return True
