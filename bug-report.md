# Testing & Bug Report - Stock Signal Alerts

## Test Execution Summary
- **Suite**: `tests/test_alerts.py` (via Python `unittest`)
- **Scope**: Mathematical SMA calculations, Wilder's RSI smoothing, Golden/Death cross detection, edge cases.
- **Result**: 7 / 7 Test Cases Passed (Execution time: 0.001s).

## Issues Identified & Fixed During Development

### Bug #1: RSI Fallback Overriding Active Trend Decisions
- **Severity**: High
- **Symptom**: `test_golden_cross_detection` failed because an active bullish trend was misclassified as `SELL`.
- **Root Cause**: When a stock experienced 20 consecutive days of gains, RSI reached 91.5 (> 78.0). Although the primary rule evaluated the Golden Cross and assigned `HOLD` (advising to wait for a dip), an unconstrained secondary RSI check ran immediately afterward and flipped the signal to `SELL`.
- **Fix**: Restricted the secondary RSI mean-reversion check to only execute when sufficient historical data for a 50-day SMA is unavailable (`curr_sma20 is None or curr_sma50 is None`).

### Bug #2: Single-Point Crossover Blind Spot
- **Severity**: Medium
- **Symptom**: If an investor ran the script on day $T+2$ after a Golden Cross, the single-day transition condition `f_prev <= s_prev and f_curr > s_curr` was already false, causing the script to miss the recent bullish breakout.
- **Fix**: Implemented `find_recent_crossover(sma_fast, sma_slow, lookback=5)` which scans a 5-day window for recent cross events before falling back to steady-state trend evaluation.

## Final Verification
```bash
python -m unittest discover -s tests -p 'test_*.py'
# Output: Ran 7 tests in 0.001s - OK
```
Both CLI table output and `--json` serialization verified.
