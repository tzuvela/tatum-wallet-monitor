import os
import json
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TATUM_API_KEY")

if not API_KEY:
    raise RuntimeError("TATUM_API_KEY not found. Check your .env file")

BASE_URL = "https://api.tatum.io"

#example Sepolia address
ADDRESS = "0x5FF137D4B0FDCD49DCA30C7CF57E578A026D2789"

def get_eth_balance(address: str) -> dict:
    url = f"{BASE_URL}/v3/ethereum/account/balance/{address}"
    headers = {"x-api-key": API_KEY}

    response = requests.get(url, headers=headers, timeout = 10)
    response.raise_for_status()

    return response.json()

def get_eth_transactions(address: str, limit: int = 5) -> dict:
    """
    Uses Tatum v4 Data API for transaction history for Sepolia address 
    Returns parsed JSON from Tatum API 
    """
    url = f"{BASE_URL}/v4/data/transaction/history"
    headers = {
        "x-api-key": API_KEY  ,
        "accept": "application/json",
    }
    params = {
        "chain": "ethereum-sepolia", 
        "addresses": address,
        "pageSize": limit,
        "sort": "DESC"
    }
    response = requests.get(url, headers=headers, params= params, timeout =15)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Fetch balance
    balance = get_eth_balance(ADDRESS)
    print("Wallet balance:")
    print(balance)

    # Fetch recent transactions, v4 endpoint:
    transactions = get_eth_transactions(ADDRESS, limit=5)
    print("\nRecent transactions:")
    print(json.dumps(transactions, indent=2))