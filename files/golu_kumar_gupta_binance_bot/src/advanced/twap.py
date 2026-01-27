import time
from src.market_orders import place_market_order
from src.utils import setup_logger, validate_positive_float, validate_symbol, validate_side

logger = setup_logger()

def place_twap_order(symbol, side, total_quantity, duration_seconds, interval_seconds):
    """
    Executes a TWAP (Time-Weighted Average Price) strategy.
    Splits the total quantity into smaller orders executed over the duration.

    Args:
        symbol (str): Trading pair.
        side (str): 'BUY' or 'SELL'.
        total_quantity (float): Total amount to trade.
        duration_seconds (int): Total time to complete execution.
        interval_seconds (int): Time between orders.
    """
    if duration_seconds <= 0 or interval_seconds <= 0:
        logger.error("Duration and interval must be positive.")
        return

    num_orders = int(duration_seconds / interval_seconds)
    if num_orders == 0:
        logger.error("Duration too short for interval.")
        return

    quantity_per_order = total_quantity / num_orders
    # Rounding might be needed depending on symbol precision info (e.g. 0.001)
    # For now simply keeping float, API might reject if precision is wrong.
    
    logger.info(f"Starting TWAP: {side} {total_quantity} {symbol} over {duration_seconds}s. "
                f"{num_orders} orders of ~{quantity_per_order:.6f} every {interval_seconds}s.")

    for i in range(num_orders):
        logger.info(f"TWAP Order {i+1}/{num_orders}")
        place_market_order(symbol, side, quantity_per_order)
        
        if i < num_orders - 1:
            time.sleep(interval_seconds)
            
    logger.info("TWAP Execution Completed")
