#!/usr/bin/env python3
"""CLI Entry point for Stock Signal Alerts."""

import argparse
import sys
from src.market_data import fetch_historical_prices
from src.strategy import evaluate_market_data
from src.notifier import format_terminal_report, format_json_report


def main():
    parser = argparse.ArgumentParser(
        description="Lightweight stock alert utility calculating SMA20/50 crossovers and RSI."
    )
    parser.add_argument(
        "--ticker", "-t",
        default="NOK",
        help="Stock ticker symbol (default: NOK - Nokia Oyj)"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=120,
        help="Number of historical trading days to evaluate (default: 120)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of human-readable terminal table"
    )

    args = parser.parse_args()

    try:
        prices = fetch_historical_prices(args.ticker, days=args.days)
        if len(prices) < 20:
            print(f"Error: Insufficient data points ({len(prices)}) for ticker '{args.ticker}'. Need at least 20.", file=sys.stderr)
            sys.exit(1)

        result = evaluate_market_data(args.ticker, prices)

        if args.json:
            print(format_json_report(result))
        else:
            print(format_terminal_report(result))

    except Exception as exc:
        print(f"Error evaluating stock signals: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
