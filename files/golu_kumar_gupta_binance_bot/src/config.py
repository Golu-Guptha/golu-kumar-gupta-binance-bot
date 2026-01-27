import os
from dotenv import load_dotenv
from binance.client import Client

# Load environment variables
load_dotenv()

def get_binance_client(testnet=True):
    """
    Initializes and returns a Binance Client.
    
    Args:
        testnet (bool): Whether to use the Testnet. Defaults to True.
    
    Returns:
        Client: An instance of the binance.client.Client
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file.")

    client = Client(api_key, api_secret, testnet=testnet)
    return client
