# Project Workflow & Requirements (PWD) - Stock Signal Alerts

## 1. Problem Statement
Retail investors and developers often miss key price trends because manual charting is tedious. A lightweight, scriptable command-line tool that evaluates established technical indicators (SMA and RSI) provides objective, automated alerts without requiring expensive paid subscriptions.

## 2. Functional Requirements
- **FR-1 Multi-Ticker Ingestion**: Support querying any global ticker (e.g. `NOK`, `AAPL`, `MSFT`, `NESTE.HE`).
- **FR-2 Technical Indicators**:
  - Calculate 20-period and 50-period moving averages.
  - Calculate 14-period Relative Strength Index (RSI).
- **FR-3 Trading Rules**:
  - **BUY**: When SMA20 crosses above SMA50 and RSI is not overbought (< 70).
  - **SELL**: When SMA20 crosses below SMA50 or RSI is overbought (> 70).
  - **HOLD**: When trends are stable with no recent crossover.
- **FR-4 Offline & Robust Execution**:
  - Gracefully handle network drops, invalid tickers, or closed markets.
  - Fall back to local fixtures when running in test mode.

## 3. Non-Functional Requirements
- **DRY & KISS**: No heavy monolithic web frameworks. Direct CLI execution.
- **Zero-Dependency Core Testing**: Unit test suite runs with standard library `unittest` out-of-the-box.
- **Speed**: Indicator computation takes under 50ms for 200 bars of historical data.
