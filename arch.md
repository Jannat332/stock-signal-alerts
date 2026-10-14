# System Architecture - Stock Signal Alerts

## Overview
`stock-signal-alerts` is a modular Python command-line utility for technical stock analysis. It ingests historical OHLCV (Open, High, Low, Close, Volume) data, calculates technical momentum indicators, evaluates deterministic trading signals, and outputs actionable trade advisories.

## Architecture Diagram

```
 +-------------------------------------------------------------+
 |                         Stock CLI                           |
 |                                                             |
 |   +--------------------+          +---------------------+   |
 |   | Market Data Feed   | -------> | Indicator Engine    |   |
 |   | (yfinance + cache) |          | (20/50 SMA, 14 RSI) |   |
 |   +--------------------+          +---------------------+   |
 |                                              |              |
 |                                              v              |
 |   +--------------------+          +---------------------+   |
 |   | Notification View  | <------- | Strategy Evaluator  |   |
 |   | (Console + JSON)   |          | (Cross & Threshold) |   |
 |   +--------------------+          +---------------------+   |
 +-------------------------------------------------------------+
```

## Component Breakdown
1. **Data Ingestion Layer (`market_data.py`)**: Fetches OHLCV historical pricing from Yahoo Finance. Includes local caching and synthetic offline mock fixtures to enable air-gapped unit testing.
2. **Indicator Compute Engine (`indicators.py`)**: Calculates rolling 20-day and 50-day Simple Moving Averages (SMA) and the 14-day Wilder's Relative Strength Index (RSI).
3. **Strategy Evaluator (`strategy.py`)**: Detects Golden Crosses (SMA20 crosses above SMA50), Death Crosses (SMA20 crosses below SMA50), and RSI Overbought (>70) / Oversold (<30) triggers.
4. **Presentation Layer (`notifier.py`)**: Formats clean, human-readable terminal dashboards and JSON alert payloads.
