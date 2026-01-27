from binance.enums import ORDER_TYPE_MARKET
from binance.exceptions import BinanceAPIException, BinanceOrderException
from src.config import get_binance_client
from src.utils import setup_logger, validate_positive_float, validate_symbol, validate_side

logger = setup_logger()

def place_market_order(symbol, side, quantity):
    """
    Places a market order on Binance Futures.

    Args:
        symbol (str): Trading pair, e.g., 'BTCUSDT'.
        side (str): 'BUY' or 'SELL'.
        quantity (float): Amount to trade.
    
    Returns:
        dict: Order response from Binance or None if failed.
    """
    try:
        # Validate inputs
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_positive_float(quantity, "quantity")

        client = get_binance_client()
        
        logger.info(f"Placing Market Order: {side} {quantity} {symbol}")
        
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        
        logger.info(f"Market Order Placed Successfully: ID {order['orderId']}, Status: {order['status']}")
        return order

    except BinanceAPIException as e:
        logger.error(f"Binance API Error: {e.status_code} - {e.message}")
    except BinanceOrderException as e:
        logger.error(f"Binance Order Error: {e.message}")
    except ValueError as e:
        logger.error(f"Validation Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
        
    return None
