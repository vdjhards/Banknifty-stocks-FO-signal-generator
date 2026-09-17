# BANKNIFTY TimesFM Signal Bot

Free/paper-trading research bot using GitHub Actions + Telegram, with 15-minute Google TimesFM 2.5 direction and 5-minute breakout confirmation.

## Important
- PAPER TRADE / RESEARCH ONLY. No profit guarantee.
- Score 0–100 is strategy strength, not probability.
- yfinance/free market data can be delayed, rate-limited, or incomplete; GitHub Actions schedules are not exact exchange-timing infrastructure.
- The bot uses BANKNIFTY index reference points, not live option-contract prices.

## Strategy
1. GitHub Actions wakes the job every 5 minutes; the Python guard runs only about one minute after each 5-minute candle closes: 09:21, 09:26, 09:31, etc. IST.
2. Ignore the forming 5-minute candle.
3. Resample completed 5-minute data to 15-minute candles and use only fully completed 15-minute windows for TimesFM.
4. TimesFM 2.5 forecasts the next 15-minute direction.
5. A 5-minute close must break prior resistance/support.
6. EMA20/EMA50, VWAP, RSI and volume confirm the setup.
7. Score must be >= 75.
8. Duplicate candle/action signals are suppressed.
9. Telegram receives only qualifying signals.

## Scan timing
The intended scan times are approximately 09:21, 09:26, 09:31, 09:36, ... IST. The minute offset is deliberate: the bot waits about one minute after the 5-minute candle closes so it does not depend on an exact GitHub Actions start time.

## Telegram
Set GitHub repository secrets:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

For local use, copy `.env.example` to `.env`.

## Install locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m src.main
```

## Accuracy
Do not assume TimesFM improves accuracy. Measure over many out-of-sample paper trades: win rate, average win/loss, profit factor, net reference points, max losing streak, score buckets, time-of-day results, and compare technical-only vs technical+TimesFM.

## TimesFM licensing
This project deliberately uses TimesFM 2.5. Check Google's current repository/license before any commercial or production use. TimesFM 3.0 weights have a more restrictive non-commercial/non-production license.
