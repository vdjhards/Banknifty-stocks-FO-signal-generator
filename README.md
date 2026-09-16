# BANKNIFTY TimesFM Signal Bot

An automated paper-trading research bot for the BANKNIFTY index. It downloads
5-minute BANKNIFTY reference data, applies a 15-minute opening-range
inside-bar breakout rule, and sends qualifying signals to Telegram.

> **Research only.** This project does not place orders and does not guarantee
> profits. Signals use the BANKNIFTY index as a reference, not live option
> contract prices.

---

## 1. Strategy: How It Works

The bot runs about every five minutes on weekdays during Indian market hours.
Each run evaluates only completed candles and sends a signal only when the
opening-range and breakout conditions agree.

### Step by step

1. **Download data** — `yfinance` requests five days of 5-minute data for
	 `^NSEBANK`.
2. **Ignore the forming candle** — timestamps are converted to `Asia/Kolkata`,
	 and the current incomplete five-minute candle is excluded.
3. **Find a coil** — candles 09:30 through 10:15 must remain fully inside the
	 09:15 candle range.
4. **Confirm the breakout** — the first 10:30–13:00 candle that closes beyond
	 the 09:15 range creates a signal. Entry is the next candle's open.
5. **Calculate paper-trade levels** — the target is 1%; the stop is the
	 opposite extreme of the 09:15 candle.
6. **Suppress duplicates** — a session and breakout combination is recorded in
	 `data/trade_journal.json`; the same signal is not sent twice.

There is no confidence score. This is a paper-trading research strategy, not a
proven edge.

---

## 2. Example Telegram Signal

```text
🚨 BANKNIFTY SIGNAL

Action: BUY CALL
Score: 85/100

BANKNIFTY: 51234.50
Entry: 51234.50
Stop Loss: 51080.20
Target 1: 51465.95
Target 2: 51665.70

15M TimesFM: BULLISH
5M Breakout: CONFIRMED

Reason: 15M TimesFM bullish + 5M resistance breakout

⚠️ PAPER TRADE — score is strategy strength, not win probability.
```

The bot sends a message only when all signal conditions pass and the
`candle|action` key has not already been recorded.

---

## 3. Setup Instructions

### A. Create a Telegram bot

1. Open Telegram and message **@BotFather**.
2. Send `/newbot` and follow the prompts.
3. Save the bot token securely.
4. Send a message to the new bot so Telegram creates a chat update.
5. Use `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` to find the chat
	 ID.

### B. Configure local secrets

Create a `.env` file in the repository root:

```dotenv
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Never commit `.env` or expose the bot token. The repository's `.gitignore`
should keep local secrets out of Git.

### C. Install locally on Windows PowerShell

Run these commands from the repository root:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m src.main
```

If PowerShell activation is restricted, run the project without activation:

```powershell
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe -m src.main
```

The bot exits quietly when it is outside 09:15–15:40 IST, on a weekend, when
market data is empty, or when no setup qualifies.

### D. Configure GitHub Actions

The workflow is stored at `.github/workflows/trading.yml`. Add these repository
secrets under **Settings → Secrets and variables → Actions**:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

The workflow currently uses Python 3.11, installs `requirements.txt`, and runs
`python -m src.main` on `ubuntu-latest`. It schedules runs every five minutes
during UTC hours 03:00–10:59, Monday through Friday, covering the intended
India market session. You can test it from **Actions → BANKNIFTY TimesFM Bot →
Run workflow**.

---

## 4. GitHub Actions Timing and Downloads

GitHub-hosted runners are normally fresh virtual machines. Each scheduled run
should be assumed to repeat checkout and dependency setup. The TimesFM model is
loaded when a run reaches forecasting and may also need to be downloaded by
the model library.

GitHub Actions schedules are best effort, not exchange-grade timing. A run can
start late, and `yfinance` data can itself be delayed or incomplete. For
research and paper trading, this workflow is convenient. For tighter timing,
use an always-on VPS or self-hosted runner where dependencies and the model can
remain cached in one environment.

---

## 5. Files and Data

| Path | Purpose |
|---|---|
| `src/main.py` | Market-hours guard, data download, orchestration, and Telegram message |
| `src/indicators.py` | Technical indicator calculations |
| `src/strategy.py` | Breakout confirmation, scoring, and trade levels |
| `src/timesfm_forecaster.py` | Lazy TimesFM model loading and direction forecast |
| `src/telegram.py` | Telegram message delivery |
| `src/journal.py` | Duplicate suppression and journal persistence |
| `src/daily_report.py` | Formats the saved journal into a daily report |
| `src/config.py` | Environment variables, symbol, timezone, and paths |
| `data/trade_journal.json` | Locally generated signal journal |
| `.github/workflows/trading.yml` | Scheduled GitHub Actions job |

The journal stores signals as `OPEN` until another process changes their
status. This project does not automatically monitor targets, stops, or option
contract outcomes.

---

## 6. Testing and Troubleshooting

Check the local environment with:

```powershell
.\\.venv\\Scripts\\python.exe -m pip check
.\\.venv\\Scripts\\python.exe -m compileall -q src
```

Test Telegram without exposing credentials:

```powershell
.\\.venv\\Scripts\\python.exe -c "from src.telegram import send; send('BANKNIFTY bot test message')"
```

Common causes of a clean run with no Telegram message:

- The current time is outside the market window.
- The latest completed candle does not break support or resistance.
- TimesFM direction is NEUTRAL or disagrees with the breakout.
- The score is below 75.
- The same candle/action signal was already recorded.

---

## 7. Known Limitations

- **Paper trading only.** No broker integration or order placement exists.
- **Index reference only.** The signal does not use live BANKNIFTY option
	contract prices, spreads, or implied volatility.
- **Data quality.** `yfinance` can be delayed, rate-limited, or incomplete.
- **Timing.** GitHub Actions schedules are not guaranteed to run exactly every
	five minutes.
- **No validated edge.** The strategy has no built-in backtest or proven win
	rate. Track win rate, average win/loss, profit factor, drawdown, losing
	streaks, score buckets, and time-of-day performance before relying on it.
- **Model availability.** TimesFM downloads and compatibility depend on the
	installed library version and network access.
- **Journal persistence.** GitHub-hosted runners are ephemeral, so a journal
	written during one run may not be available to the next run unless it is
	stored externally or committed, which is not configured here.
- **Licensing.** Check Google's current TimesFM repository and model license
	before commercial or production use. TimesFM 3.0 weights have more
	restrictive non-commercial and non-production terms.
