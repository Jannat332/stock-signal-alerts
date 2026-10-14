# Engineering Rules & Guidelines - Stock Signal Alerts

## 1. Principles
- **KISS**: Avoid over-engineered quantitative frameworks or complex async event loops for a single-ticker query. A straightforward procedural pipeline (`Fetch -> Compute -> Evaluate -> Display`) is easier to read and maintain.
- **DRY**: Shared moving average calculations reuse a single rolling window function (`calculate_sma(prices, window)`).

## 2. Python Standards
- Python 3.9+ compatible (`dataclasses`, type hints `Optional`, `List`, `Tuple`).
- Standard PEP 8 naming (`snake_case` functions, `PascalCase` classes).
- Proper exception handling around network and data formatting errors.
- Never hardcode API keys or credentials.
- No AI fluff comments (e.g. avoid `// Loop through prices`). Use clean docstrings explaining inputs and return types.
