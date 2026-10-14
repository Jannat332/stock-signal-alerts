"""Technical indicator mathematical computation module."""

from typing import List, Optional


def calculate_sma(prices: List[float], window: int) -> List[Optional[float]]:
    """Calculates the Simple Moving Average over a rolling window.
    
    Returns a list of the same length as prices, padded with None for 
    indices where fewer than 'window' data points exist.
    """
    if window <= 0:
        raise ValueError("Window size must be greater than zero.")
    
    smas: List[Optional[float]] = []
    running_sum = 0.0

    for i, p in enumerate(prices):
        running_sum += p
        if i >= window:
            running_sum -= prices[i - window]
        
        if i >= window - 1:
            smas.append(round(running_sum / window, 4))
        else:
            smas.append(None)

    return smas


def calculate_rsi(prices: List[float], period: int = 14) -> List[Optional[float]]:
    """Calculates Relative Strength Index (RSI) using Wilder's smoothing.
    
    Returns a list matching prices length, padded with None until sufficient
    periods are available.
    """
    if period <= 0:
        raise ValueError("Period must be greater than zero.")
    if len(prices) <= period:
        return [None] * len(prices)

    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    rsi_values: List[Optional[float]] = [None]  # first price has no delta

    gains = [max(d, 0.0) for d in deltas]
    losses = [max(-d, 0.0) for d in deltas]

    # First average
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period - 1):
        rsi_values.append(None)

    if avg_loss == 0.0:
        rsi_values.append(100.0)
    else:
        rs = avg_gain / avg_loss
        rsi_values.append(round(100.0 - (100.0 / (1.0 + rs)), 2))

    # Wilder's smoothing for remaining
    for i in range(period, len(deltas)):
        gain = gains[i]
        loss = losses[i]

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0.0:
            rsi_values.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsi_values.append(round(100.0 - (100.0 / (1.0 + rs)), 2))

    return rsi_values
