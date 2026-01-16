import os
import json
import requests
from requests.exceptions import HTTPError
from requests.exceptions import ReadTimeout
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
API_KEY = os.getenv("TATUM_API_KEY")

if not API_KEY:
    raise RuntimeError("TATUM_API_KEY not found. Check your .env file")

BASE_URL = "https://api.tatum.io"

#example Sepolia address
CHAIN = os.getenv("CHAIN")
ADDRESS = os.getenv("WALLET_ADDRESS")
if not CHAIN:
     raise RuntimeError("CHAIN not set in .env")
if not ADDRESS:
     raise RuntimeError("ADDRESS not set in .env")

session = requests.Session()
session.headers.update({"x-api-key": API_KEY, "accept": "application/json"})

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
        "chain": CHAIN, 
        "addresses": [address],
        "pageSize": limit,
        "sort": "DESC"
    }
    try:
            response = requests.get(url, headers=headers, params= params, timeout =(3, 15))
            response.raise_for_status()
            return response.json()
    except ReadTimeout:
         print("Transaction fetch timed out")
         return{"result": []}

def print_transactions(transactions: dict, truncate: bool = True):
    print("\nRecent transactions:")
    for tx in transactions.get("result", []):
        if truncate:
                short_hash = tx["hash"][:10] + "..."
                from_addr = tx["counterAddress"][:10] + "..."
                to_addr = tx["address"][:10] + "..."
        else:
             short_hash = tx["hash"]
             from_addr = tx["counterAddress"]
             to_addr = tx["address"]
        amount = tx["amount"]
        block = tx["blockNumber"]

        ts = datetime.fromtimestamp(int(tx["timestamp"])/1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{short_hash} | {from_addr} -> {to_addr} | {amount} | Block {block} | {ts}")

if __name__ == "__main__":
    # Fetch balance
    balance = get_eth_balance(ADDRESS)
    print("Wallet balance:")
    print(balance)

    # Fetch recent transactions, v4 endpoint:
    transactions = get_eth_transactions(ADDRESS, limit=5)
    print_transactions(transactions)