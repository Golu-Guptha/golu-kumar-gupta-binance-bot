from binance.exceptions import BinanceAPIException
from src.config import get_binance_client
from src.utils import setup_logger, validate_positive_float, validate_symbol, validate_side

logger = setup_logger()

# Constants
ORDER_TYPE_STOP_MARKET = 'STOP_MARKET'
ORDER_TYPE_TAKE_PROFIT_MARKET = 'TAKE_PROFIT_MARKET'

def place_oco_order(symbol, side, quantity, stop_price, take_profit_price):
    """
    Places a One-Cancels-the-Other (OCO) equivalent strategy for Futures.
    Creates a Stop Loss and a Take Profit order.
    
    Args:
        symbol (str): Trading pair.
        side (str): 'BUY' or 'SELL'. IMPORTANT: This is the side of the ENTRY position,
                    so TP/SL will be the OPPOSITE side.
        quantity (float): Quantity of the position.
        stop_price (float): Stop Loss trigger price.
        take_profit_price (float): Take Profit trigger price.
    """
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_positive_float(quantity, "quantity")
        stop_price = validate_positive_float(stop_price, "stop_price")
        take_profit_price = validate_positive_float(take_profit_price, "take_profit_price")
        
        # In Futures, TP/SL limit/market orders to close a position are of the OPPOSITE side.
        # If we entered BUY (Long), we close with SELL.
        close_side = "SELL" if side == "BUY" else "BUY"
        
        client = get_binance_client()
        logger.info(f"Placing OCO for {symbol} (Position: {side}). Close Side: {close_side}")

        # 1. Place Stop Loss
        stop_order = client.futures_create_order(
            symbol=symbol,
            side=close_side,
            type=ORDER_TYPE_STOP_MARKET,
            stopPrice=stop_price,
            quantity=quantity,
            reduceOnly=True
        )
        logger.info(f"Stop Loss Placed: {stop_order.get('orderId') or stop_order.get('algoId')} at {stop_price}")

        # 2. Place Take Profit
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=close_side,
            type=ORDER_TYPE_TAKE_PROFIT_MARKET,
            stopPrice=take_profit_price, # Parameter is often stopPrice or price depending on type
            quantity=quantity,
            reduceOnly=True
        )
        logger.info(f"Take Profit Placed: {tp_order.get('orderId') or tp_order.get('algoId')} at {take_profit_price}")
        
        return {"stop_loss": stop_order, "take_profit": tp_order}

    except BinanceAPIException as e:
        logger.error(f"Binance API Error (OCO): {e.status_code} - {e.message}")
    except Exception as e:
        logger.error(f"Error placing OCO: {str(e)}")
        
    return None
