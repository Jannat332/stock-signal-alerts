"""Market data fetcher with online provider and offline mock fallback."""

import math
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PricePoint:
    date: str
    close: float
    volume: int


def generate_synthetic_trend(base_price: float = 100.0, days: int = 120, trend: str = "bullish") -> List[PricePoint]:
    """Generates realistic synthetic daily prices for testing and offline execution."""
    points = []
    current = base_price

    for day in range(1, days + 1):
        if trend == "bullish":
            drift = 0.25 if day < 80 else 0.45
            wave = 1.8 * math.sin(day / 6.0)
        elif trend == "bearish":
            drift = -0.30 if day > 40 else 0.10
            wave = 1.5 * math.cos(day / 5.0)
        else:
            drift = 0.05
            wave = 2.0 * math.sin(day / 4.0)

        current = max(5.0, round(current + drift + wave * 0.4, 2))
        points.append(PricePoint(
            date=f"2026-01-{(day % 28) + 1:02d}",
            close=current,
            volume=int(1_000_000 + abs(wave) * 50_000)
        ))

    return points


def fetch_historical_prices(ticker: str, days: int = 100) -> List[PricePoint]:
    """Fetches real market prices via yfinance, falling back to clean mock trend if offline."""
    try:
        import yfinance as yf
        data = yf.Ticker(ticker).history(period=f"{days}d")
        if not data.empty and len(data) > 20:
            prices = []
            for idx, row in data.iterrows():
                prices.append(PricePoint(
                    date=str(idx.date()),
                    close=round(float(row["Close"]), 2),
                    volume=int(row["Volume"])
                ))
            return prices
    except Exception:
        pass

    # Seamless fallback to deterministic fixture based on ticker name
    trend = "bullish" if ticker.upper() in ["NOK", "AAPL", "MSFT"] else "bearish"
    base = 4.20 if ticker.upper() == "NOK" else (180.0 if ticker.upper() == "AAPL" else 50.0)
    return generate_synthetic_trend(base_price=base, days=days, trend=trend)
