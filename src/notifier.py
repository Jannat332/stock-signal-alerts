"""Output formatting and terminal reporting module."""

import json
from src.strategy import AlertResult, SignalType


def format_terminal_report(result: AlertResult) -> str:
    """Formats a clean terminal card with status icons and indicators."""
    badge = {
        SignalType.BUY:  "[BUY ALERT]",
        SignalType.SELL: "[SELL ALERT]",
        SignalType.HOLD: "[HOLD / NEUTRAL]"
    }[result.signal]

    lines = [
        "=" * 60,
        f"  STOCK SIGNAL REPORT: {result.ticker}  |  {badge}",
        "=" * 60,
        f"  Latest Close:  ${result.latest_price:.2f}  (As of {result.latest_date})",
        f"  SMA 20-Day:    ${result.sma20:.2f}" if result.sma20 else "  SMA 20-Day:    N/A",
        f"  SMA 50-Day:    ${result.sma50:.2f}" if result.sma50 else "  SMA 50-Day:    N/A",
        f"  RSI 14-Day:    {result.rsi14:.1f}" if result.rsi14 else "  RSI 14-Day:    N/A",
        "-" * 60,
        f"  Action:        {result.signal.value}",
        f"  Rationale:     {result.rationale}",
        "=" * 60,
    ]
    return "\n".join(lines)


def format_json_report(result: AlertResult) -> str:
    """Serializes alert result into structured JSON for downstream automation."""
    payload = {
        "ticker": result.ticker,
        "date": result.latest_date,
        "price": result.latest_price,
        "indicators": {
            "sma20": result.sma20,
            "sma50": result.sma50,
            "rsi14": result.rsi14,
        },
        "signal": result.signal.value,
        "rationale": result.rationale
    }
    return json.dumps(payload, indent=2)
