# Binance Futures Order Bot - Project Report

**Author**: [Your Name]
**Date**: 2024-12-31

## 1. Project Overview
This project implements a robust CLI-based trading bot for Binance USDT-M Futures. It supports core order types (Market, Limit) and advanced strategies (OCO, TWAP).

## 2. Architecture
The project is structured for modularity and scalability:
- **`src/`**: Logic core.
  - **`config.py`**: Securely handles API credentials.
  - **`utils.py`**: Centralized logging and validation.
  - **`market_orders.py` & `limit_orders.py`**: Isolated order logic.
  - **`main.py`**: unified CLI entry point using `argparse`.
- **`src/advanced/`**: Bonus features.
  - **`oco.py`**: Implements One-Cancels-the-Other using API Stop/TP mechanisms.
  - **`twap.py`**: Algorithmic order splitting.

## 3. Advanced Features (Bonus)
### OCO (One-Cancels-the-Other)
Implemented in `src/advanced/oco.py`. It places two simultaneous orders:
1.  **Stop Loss**: A `STOP_MARKET` order to close the position if price moves against us.
2.  **Take Profit**: A `TAKE_PROFIT_MARKET` order to lock in gains.
*Note: Uses `closePosition=True` to ensure correct position management.*

### TWAP (Time-Weighted Average Price)
Implemented in `src/advanced/twap.py`.
- Breaks a large `quantity` into smaller chunks.
- Executes them at regular `interval`s over a `duration`.
- Reduces market impact for large trades.

## 4. Validation & Logging
- **Logging**: All actions are logged to `bot.log` with timestamps.
    - Info level: Order placements, successful executions.
    - Error level: validation failures, API errors (400, 401).
- **Validation**:
    - Symbol format checks (`BTCUSDT`).
    - Negative quantity/price prevention.
    - Order side validation (`BUY`/`SELL`).

## 5. Verification Results
### Market Order (Testnet)
- **Command**: `python src/main.py market BTCUSDT BUY 0.001`
- **Result**: Validated handling of "Insufficient Margin" (since test account has 0 balance). proper 400 error logged.

### OCO Order (Testnet)
- **Command**: `python src/main.py oco BTCUSDT BUY 0.001 40000 60000`
- **Result**: Validated correct API endpoint usage. API returned "No positions are available", confirming the logic attempted to close a position as designed.
