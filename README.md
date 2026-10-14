# Stock Signal Alerts (Python)

A lightweight command-line stock analysis tool that evaluates technical indicators (20-day & 50-day Simple Moving Average crossovers and 14-day Relative Strength Index) to generate actionable `BUY`, `SELL`, and `HOLD` advisories.

---

## Features
- **Moving Average Crossover Detection**: Identifies Bullish Golden Crosses (SMA20 crossing above SMA50) and Bearish Death Crosses (SMA20 crossing below SMA50) across a configurable lookback window.
- **RSI Momentum Filter**: Calculates 14-period Wilder's RSI to prevent buying into exhausted overbought tops or selling into deeply oversold bottoms.
- **Multi-Ticker Support**: Works with US and international tickers (e.g. `NOK`, `AAPL`, `MSFT`, `NESTE.HE`).
- **Offline & Testing Resilient**: Seamlessly falls back to deterministic historical price fixtures if working offline.
- **JSON Automation Flag**: Emits structured JSON via `--json` for integration into automated alerting scripts or Telegram bots.

---

## Project Structure
```
02-stock-signal-alerts/
├── src/
│   ├── indicators.py   # Pure Python SMA & RSI mathematical routines
│   ├── market_data.py  # Yahoo Finance fetcher with offline mock fallback
│   ├── strategy.py     # Crossover detection & trading rule evaluation
│   └── notifier.py     # Terminal card formatting & JSON serializer
├── tests/
│   └── test_alerts.py  # Automated test suite (Python unittest)
├── main.py             # CLI entrypoint with argument parser
├── requirements.txt    # Optional dependencies (yfinance, pandas)
├── arch.md             # System architecture & component diagram
├── pwd.md              # Requirements and workflow documentation
├── design.md           # Mathematical formulas and data models
├── memory.md           # Engineering decisions and tradeoffs
├── rules.md            # Coding standards & DRY/KISS principles
└── bug-report.md       # Test logs & bug fixes documented during development
```

---

## Quickstart

### Prerequisites
- Python 3.9+
- Optional: `pip install -r requirements.txt` (for real-time Yahoo Finance queries)

### Running the CLI
```bash
# Analyze default ticker (NOK - Nokia)
python main.py

# Analyze a specific stock with custom lookback period
python main.py --ticker AAPL --days 150

# Output structured JSON for automation
python main.py --ticker MSFT --json
```

### Running Unit Tests
The test suite has zero third-party dependencies and runs natively with Python's standard library:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## Technical Indicator Strategy Summary
- **🟢 BUY**: SMA20 crosses above SMA50 (Golden Cross) with RSI < 70, OR established bullish trend with stable RSI.
- **🔴 SELL**: SMA20 drops below SMA50 (Death Cross), OR sustained bearish trend alignment.
- **⚪ HOLD**: Overbought RSI warning (> 75), consolidation range, or insufficient historical data.

---

## License
MIT License.
