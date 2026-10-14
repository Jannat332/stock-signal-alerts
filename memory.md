# Memory & Decision Log - Stock Signal Alerts

## Context & Key Decisions
- **Decision 1: Pure Python Mathematical Fallback**
  - *Rationale*: While `pandas` and `numpy` are great, having lightweight standard-library math routines allows the indicator algorithms to be unit-tested in environments where heavy compiled wheels are not installed.
- **Decision 2: Separation of Data Fetching from Strategy Logic**
  - *Rationale*: Coupling Yahoo Finance API calls inside the indicator class makes unit tests dependent on network connectivity. By separating `market_data.py` from `strategy.py`, we test mathematical edge cases with deterministic static price arrays.
- **Decision 3: Handling Insufficient Data Periods Gracefully**
  - *Rationale*: A stock with only 10 days of history cannot compute a 50-day SMA. The system returns `None` for unavailable indicators and flags `HOLD` with a clear user advisory rather than crashing with an `IndexError`.
