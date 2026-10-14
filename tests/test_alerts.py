"""Automated unit test suite for stock signal calculations."""

import unittest
from src.indicators import calculate_sma, calculate_rsi
from src.market_data import PricePoint
from src.strategy import evaluate_market_data, SignalType


class TestIndicatorCalculations(unittest.TestCase):

    def test_sma_basic(self):
        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        sma3 = calculate_sma(prices, window=3)
        self.assertIsNone(sma3[0])
        self.assertIsNone(sma3[1])
        self.assertAlmostEqual(sma3[2], 20.0)  # (10+20+30)/3
        self.assertAlmostEqual(sma3[3], 30.0)  # (20+30+40)/3
        self.assertAlmostEqual(sma3[4], 40.0)  # (30+40+50)/3

    def test_sma_invalid_window(self):
        with self.assertRaises(ValueError):
            calculate_sma([1.0, 2.0], window=0)

    def test_rsi_bounds(self):
        # Monotonically increasing prices -> RSI should be high (>70)
        increasing = [float(10 + i * 2) for i in range(30)]
        rsi = calculate_rsi(increasing, period=14)
        latest_rsi = rsi[-1]
        self.assertIsNotNone(latest_rsi)
        self.assertGreater(latest_rsi, 70.0)
        self.assertLessEqual(latest_rsi, 100.0)

    def test_rsi_all_down(self):
        # Monotonically decreasing prices -> RSI should be low (<30)
        decreasing = [float(100 - i * 2) for i in range(30)]
        rsi = calculate_rsi(decreasing, period=14)
        latest_rsi = rsi[-1]
        self.assertIsNotNone(latest_rsi)
        self.assertLess(latest_rsi, 30.0)


class TestStrategyEvaluation(unittest.TestCase):

    def test_golden_cross_detection(self):
        # Create a series where fast SMA crosses above slow SMA
        prices = []
        # First 60 days flat at 10.0
        for i in range(60):
            prices.append(PricePoint(date=f"2026-01-{i+1:02d}", close=10.0, volume=1000))
        # Next 20 days sharp rise to 30.0 -> SMA20 will cross above SMA50
        for i in range(20):
            prices.append(PricePoint(date=f"2026-03-{i+1:02d}", close=10.0 + (i + 1) * 1.5, volume=2000))

        result = evaluate_market_data("TEST", prices)
        # Should detect bullish momentum / golden cross
        self.assertIn(result.signal, [SignalType.BUY, SignalType.HOLD])
        self.assertIsNotNone(result.sma20)
        self.assertIsNotNone(result.sma50)

    def test_death_cross_detection(self):
        prices = []
        for i in range(60):
            prices.append(PricePoint(date=f"2026-01-{i+1:02d}", close=50.0, volume=1000))
        for i in range(20):
            prices.append(PricePoint(date=f"2026-03-{i+1:02d}", close=50.0 - (i + 1) * 1.8, volume=2000))

        result = evaluate_market_data("BEAR", prices)
        self.assertIn(result.signal, [SignalType.SELL, SignalType.HOLD])

    def test_insufficient_data(self):
        short_series = [PricePoint(date="2026-01-01", close=10.0, volume=100)]
        result = evaluate_market_data("MINI", short_series)
        self.assertEqual(result.signal, SignalType.HOLD)
        self.assertIsNone(result.sma20)
        self.assertIsNone(result.sma50)


if __name__ == "__main__":
    unittest.main()
