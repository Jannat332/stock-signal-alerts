# Software Design Specification - Stock Signal Alerts

## Data Structures
```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

@dataclass
class PriceBar:
    date: str
    close: float
    volume: int

@dataclass
class TechnicalReport:
    ticker: str
    latest_price: float
    sma20: Optional[float]
    sma50: Optional[float]
    rsi14: Optional[float]
    signal: Signal
    reason: str
```

## Mathematical Formulas
1. **Simple Moving Average (SMA)**:
   $$SMA_k(t) = \frac{1}{k} \sum_{i=0}^{k-1} P(t-i)$$
2. **Relative Strength Index (RSI)**:
   $$RS = \frac{\text{Average Gain over } 14 \text{ periods}}{\text{Average Loss over } 14 \text{ periods}}$$
   $$RSI = 100 - \left( \frac{100}{1 + RS} \right)$$

## Crossover Detection Algorithm
```python
def evaluate_crossover(sma_fast_current, sma_fast_prev, sma_slow_current, sma_slow_prev, rsi):
    if sma_fast_prev <= sma_slow_prev and sma_fast_current > sma_slow_current:
        if rsi is None or rsi < 70.0:
            return Signal.BUY, "Golden Cross (SMA20 broke above SMA50)"
    if sma_fast_prev >= sma_slow_prev and sma_fast_current < sma_slow_current:
        return Signal.SELL, "Death Cross (SMA20 dropped below SMA50)"
    if rsi is not None and rsi > 75.0:
        return Signal.SELL, f"Overbought territory (RSI={rsi:.1f} > 75)"
    if rsi is not None and rsi < 25.0:
        return Signal.BUY, f"Oversold bounce potential (RSI={rsi:.1f} < 25)"
    return Signal.HOLD, "Trend neutral or ongoing"
```
