import logging
import sys

def setup_logger(name="binance_bot", log_file="bot.log"):
    """
    Sets up a logger that executes to both console and file.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        # File Handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter('%(message)s') # Simpler format for console
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

    return logger

def validate_positive_float(value, name):
    """
    Validates that a value is a positive float.
    
    Args:
        value (str or float): The value to validate.
        name (str): The name of the field for error messages.
        
    Returns:
        float: The validated float value.
        
    Raises:
        ValueError: If validation fails.
    """
    try:
        f_value = float(value)
        if f_value <= 0:
            raise ValueError(f"{name} must be greater than 0.")
        return f_value
    except ValueError as e:
        raise ValueError(f"Invalid {name}: {e}")

def validate_symbol(symbol):
    """
    Basic validation for symbol format.
    
    Args:
        symbol (str): The trading symbol (e.g., BTCUSDT).
    
    Returns:
        str: Upper-cased symbol.
    """
    if not isinstance(symbol, str) or len(symbol) < 5:
        raise ValueError(f"Invalid symbol format: {symbol}")
    return symbol.upper()

def validate_side(side):
    """
    Validates order side.
    
    Args:
        side (str): 'BUY' or 'SELL'.
    
    Returns:
        str: Upper-cased side.
    """
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL.")
    return side
