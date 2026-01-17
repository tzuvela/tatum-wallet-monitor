import os
import json
import csv
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

# example Sepolia address
CHAIN = os.getenv("CHAIN")
if not CHAIN:
    raise RuntimeError("CHAIN not set in .env")
ADDRESS = os.getenv("WALLET_ADDRESS")
if not ADDRESS:
    raise RuntimeError("ADDRESS not set in .env")

session = requests.Session()
session.headers.update({"x-api-key": API_KEY, "accept": "application/json"})

def get_eth_balance(address: str) -> dict:
    url = f"{BASE_URL}/v3/ethereum/account/balance/{address}"
    headers = {"x-api-key": API_KEY}

    response = session.get(url, headers=headers, timeout = 10)
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
        response = session.get(url, headers= headers, params= params, timeout= (3, 20))
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

def export_transactions(transactions: dict, filename: str = "transactions.csv"):
    fields = [
        "timestamp",
        "hash",
        "from_address",
        "to_address",
        "amount",
        "block",
        "chain"
    ]

    with open(filename, mode ="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for tx in transactions.get("result", []):
            ts = datetime.fromtimestamp(
                int(tx["timestamp"]) /1000,
                tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow({
                "timestamp": ts,
                "hash": tx["hash"],
                "from_address": tx["counterAddress"],
                "to_address": tx["address"],
                "amount": tx["amount"],
                "block": tx["blockNumber"],
                "chain": tx["chain"]

            })
        print(f"Transactions exported to {filename}")
if __name__ == "__main__":
    # Fetch balance
    balance = get_eth_balance(ADDRESS)
    print("Wallet balance:")
    print(balance)

    # Fetch recent transactions, v4 endpoint:
    transactions = get_eth_transactions(ADDRESS, limit=5)
    print_transactions(transactions)
    export_transactions(transactions)