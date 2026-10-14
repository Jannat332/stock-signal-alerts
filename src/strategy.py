"""Trading strategy evaluation module."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from src.indicators import calculate_sma, calculate_rsi
from src.market_data import PricePoint


class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class AlertResult:
    ticker: str
    latest_date: str
    latest_price: float
    sma20: Optional[float]
    sma50: Optional[float]
    rsi14: Optional[float]
    signal: SignalType
    rationale: str


def find_recent_crossover(sma_fast: List[Optional[float]], sma_slow: List[Optional[float]], lookback: int = 5) -> Optional[str]:
    """Scans the last 'lookback' periods for a Golden Cross or Death Cross."""
    max_idx = len(sma_fast)
    start_idx = max(1, max_idx - lookback)

    for i in range(start_idx, max_idx):
        f_prev, f_curr = sma_fast[i - 1], sma_fast[i]
        s_prev, s_curr = sma_slow[i - 1], sma_slow[i]

        if f_prev is not None and s_prev is not None and f_curr is not None and s_curr is not None:
            if f_prev <= s_prev and f_curr > s_curr:
                return "GOLDEN_CROSS"
            elif f_prev >= s_prev and f_curr < s_curr:
                return "DEATH_CROSS"
    return None


def evaluate_market_data(ticker: str, prices: List[PricePoint]) -> AlertResult:
    """Evaluates moving average crossovers, trend direction, and RSI momentum."""
    if not prices:
        raise ValueError("Price list cannot be empty.")

    closes = [p.close for p in prices]
    latest = prices[-1]

    sma20 = calculate_sma(closes, window=20)
    sma50 = calculate_sma(closes, window=50)
    rsi14 = calculate_rsi(closes, period=14)

    curr_sma20 = sma20[-1]
    curr_sma50 = sma50[-1]
    curr_rsi = rsi14[-1]

    recent_crossover = find_recent_crossover(sma20, sma50, lookback=5)

    signal = SignalType.HOLD
    rationale = "No decisive crossover detected. Market in consolidation."

    if curr_sma20 is not None and curr_sma50 is not None:
        if recent_crossover == "GOLDEN_CROSS":
            if curr_rsi is not None and curr_rsi > 75.0:
                signal = SignalType.HOLD
                rationale = f"Recent Golden Cross detected, but RSI={curr_rsi:.1f} is overbought. Wait for healthy dip."
            else:
                signal = SignalType.BUY
                rationale = f"Recent Golden Cross! SMA20 ({curr_sma20}) broke above SMA50 ({curr_sma50}). Bullish momentum."
        elif recent_crossover == "DEATH_CROSS":
            signal = SignalType.SELL
            rationale = f"Recent Death Cross! SMA20 ({curr_sma20}) dropped below SMA50 ({curr_sma50}). Downtrend confirmed."
        elif curr_sma20 > curr_sma50:
            # Established bullish trend
            if curr_rsi is not None and curr_rsi > 78.0:
                signal = SignalType.HOLD
                rationale = f"Bullish trend active (SMA20 > SMA50), but RSI={curr_rsi:.1f} shows stretched overbought territory."
            else:
                signal = SignalType.BUY
                rationale = f"Bullish alignment: SMA20 ({curr_sma20}) is above SMA50 ({curr_sma50}) with stable RSI ({curr_rsi or 'N/A'})."
        elif curr_sma20 < curr_sma50:
            # Established bearish trend
            signal = SignalType.SELL
            rationale = f"Bearish alignment: SMA20 ({curr_sma20}) is below SMA50 ({curr_sma50}). Avoid or take profit."

    # Fallback check: If insufficient history for 50-day SMA, evaluate extreme RSI
    elif curr_rsi is not None:
        if curr_rsi < 25.0:
            signal = SignalType.BUY
            rationale = f"Deeply oversold (RSI={curr_rsi:.1f}). Potential short-term mean reversion bounce."
        elif curr_rsi > 78.0:
            signal = SignalType.SELL
            rationale = f"Extreme overbought (RSI={curr_rsi:.1f}). Risk of downward correction."

    return AlertResult(
        ticker=ticker.upper(),
        latest_date=latest.date,
        latest_price=latest.close,
        sma20=curr_sma20,
        sma50=curr_sma50,
        rsi14=curr_rsi,
        signal=signal,
        rationale=rationale
    )
