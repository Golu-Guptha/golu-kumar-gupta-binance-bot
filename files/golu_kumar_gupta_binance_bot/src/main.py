import argparse
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.oco import place_oco_order
from src.advanced.twap import place_twap_order
from src.utils import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Market Order Parser
    market_parser = subparsers.add_parser("market", help="Place a Market Order")
    market_parser.add_argument("symbol", type=str, help="Trading Pair (e.g., BTCUSDT)")
    market_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Order Side")
    market_parser.add_argument("quantity", type=float, help="Quantity to trade")

    # Limit Order Parser
    limit_parser = subparsers.add_parser("limit", help="Place a Limit Order")
    limit_parser.add_argument("symbol", type=str, help="Trading Pair (e.g., BTCUSDT)")
    limit_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Order Side")
    limit_parser.add_argument("quantity", type=float, help="Quantity to trade")
    limit_parser.add_argument("price", type=float, help="Limit Price")

    # OCO Order Parser
    oco_parser = subparsers.add_parser("oco", help="Place OCO Order (Stop Loss + Take Profit)")
    oco_parser.add_argument("symbol", type=str, help="Trading Pair")
    oco_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Position Side (e.g. BUY for Long)")
    oco_parser.add_argument("quantity", type=float, help="Quantity")
    oco_parser.add_argument("stop_price", type=float, help="Stop Loss Trigger Price")
    oco_parser.add_argument("tp_price", type=float, help="Take Profit Trigger Price")

    # TWAP Order Parser
    twap_parser = subparsers.add_parser("twap", help="Execute TWAP Strategy")
    twap_parser.add_argument("symbol", type=str, help="Trading Pair")
    twap_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Side")
    twap_parser.add_argument("quantity", type=float, help="Total Quantity")
    twap_parser.add_argument("duration", type=int, help="Total Duration (seconds)")
    twap_parser.add_argument("interval", type=int, help="Interval between orders (seconds)")

    # Cancel All Parser
    cancel_parser = subparsers.add_parser("cancel", help="Cancel All Open Orders for Symbol")
    cancel_parser.add_argument("symbol", type=str, help="Trading Pair")

    # Balance/Test Parser
    subparsers.add_parser("balance", help="Check Account Balance (Test Connection)")

    # If no arguments provided, show interactive menu
    if len(sys.argv) == 1:
        print("Welcome to Binance Futures Bot!")
        print("1. Market Order")
        print("2. Limit Order")
        print("3. OCO Order")
        print("4. TWAP Strategy")
        print("5. Check Balance")
        print("6. Cancel All Orders")
        print("7. Exit")
        
        choice = input("Select an option (1-7): ")
        
        if choice == '1':
            symbol = input("Symbol (e.g., BTCUSDT): ")
            side = input("Side (BUY/SELL): ")
            qty = float(input("Quantity: "))
            place_market_order(symbol, side, qty)
            return
        elif choice == '2':
            symbol = input("Symbol (e.g., BTCUSDT): ")
            side = input("Side (BUY/SELL): ")
            qty = float(input("Quantity: "))
            price = float(input("Price: "))
            place_limit_order(symbol, side, qty, price)
            return
        elif choice == '3':
            symbol = input("Symbol: ")
            side = input("Position Side (BUY/SELL): ")
            qty = float(input("Quantity: "))
            stop = float(input("Stop Price: "))
            tp = float(input("Take Profit Price: "))
            place_oco_order(symbol, side, qty, stop, tp)
            return
        elif choice == '4':
            symbol = input("Symbol: ")
            side = input("Side: ")
            qty = float(input("Total Quantity: "))
            duration = int(input("Duration (s): "))
            interval = int(input("Interval (s): "))
            place_twap_order(symbol, side, qty, duration, interval)
            return
        elif choice == '5':
            # Simulate args for balance
            class MockArgs: command = 'balance'
            args = MockArgs()
        elif choice == '6':
            symbol = input("Symbol to Cancel All: ")
            from src.config import get_binance_client
            try:
                client = get_binance_client()
                logger.info(f"Cancelling all open orders for {symbol}...")
                client.futures_cancel_all_open_orders(symbol=symbol)
                logger.info("All open orders cancelled successfully.")
            except Exception as e:
                logger.error(f"Failed to cancel orders: {str(e)}")
            return
        elif choice == '7':
            sys.exit(0)
        else:
            print("Invalid choice.")
            sys.exit(1)
    else:
        args = parser.parse_args()

    if getattr(args, 'command', None) == "market":
        place_market_order(args.symbol, args.side, args.quantity)
    elif getattr(args, 'command', None) == "limit":
        place_limit_order(args.symbol, args.side, args.quantity, args.price)
    elif getattr(args, 'command', None) == "oco":
        place_oco_order(args.symbol, args.side, args.quantity, args.stop_price, args.tp_price)
    elif getattr(args, 'command', None) == "twap":
        place_twap_order(args.symbol, args.side, args.quantity, args.duration, args.interval)
    elif getattr(args, 'command', None) == "cancel":
        from src.config import get_binance_client
        try:
            client = get_binance_client()
            logger.info(f"Cancelling all open orders for {args.symbol}...")
            client.futures_cancel_all_open_orders(symbol=args.symbol)
            logger.info("All open orders cancelled successfully.")
        except Exception as e:
            logger.error(f"Failed to cancel orders: {str(e)}")
    elif getattr(args, 'command', None) == "balance":
        from src.config import get_binance_client
        try:
            client = get_binance_client()
            balance = client.futures_account_balance()
            # Filter for USDT
            usdt_balance = next((item for item in balance if item["asset"] == "USDT"), None)
            if usdt_balance:
                logger.info(f"Connection Successful!")
                logger.info(f"Wallet Balance: {usdt_balance['balance']}")
                logger.info(f"Available Balance: {usdt_balance.get('availableBalance', 'N/A')}")
            else:
                logger.info("Connection Successful! Could not find USDT balance.")
        except Exception as e:
            logger.error(f"Connection Failed: {str(e)}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
