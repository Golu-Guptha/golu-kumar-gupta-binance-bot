# Binance Futures Order Bot

A CLI-based trading bot for Binance USDT-M Futures.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory with your Binance Testnet credentials:
    ```env
    BINANCE_API_KEY=your_api_key
    BINANCE_API_SECRET=your_api_secret
    ```
    *Note: Use Testnet credentials from [Binance Futures Testnet](https://testnet.binancefuture.com/en/futures/BTCUSDT).*

## Usage

### Market Order
```bash
python src/main.py market BTCUSDT BUY 0.001
```

### Limit Order
```bash
python src/main.py limit BTCUSDT BUY 0.001 50000
```

### Limit Order
```bash
python src/main.py limit BTCUSDT BUY 0.001 50000
```

### OCO Order (Advanced)
Places a Stop Loss and Take Profit for an existing position.
```bash
python src/main.py oco BTCUSDT BUY 0.001 40000 60000
# Format: oco [SYMBOL] [POSITION_SIDE] [QUANTITY] [STOP_PRICE] [TP_PRICE]
```

### TWAP Strategy (Advanced)
Splits an order over time.
```bash
python src/main.py twap BTCUSDT BUY 0.01 60 10
# Format: twap [SYMBOL] [SIDE] [TOTAL_QTY] [DURATION_SEC] [INTERVAL_SEC]
```

### check balance
```bash
python src/main.py balance
```

### Interactive Mode (New!)
Run without arguments to use the menu:
```bash
python src/main.py
```

## Structure
- `src/`: Source code
- `src/advanced/`: OCO and TWAP logic
- `bot.log`: Log file (records all API calls and errors)
- `report.md`: Project report and analysis
