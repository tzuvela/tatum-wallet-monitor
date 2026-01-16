import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TATUM_API_KEY")

if not API_KEY:
    raise RuntimeError("TATUM_API_KEY not found. Check your .env file")

BASE_URL = "https://api.tatum.io"

#example Ethereum test address
ADDRESS = "0x0000000000000000000000000000000000000000"

def get_eth_balance(address: str) -> dict:
    url = f"{BASE_URL}/v3/ethereum/account/balance/{address}"
    headers = {
        "x-api-key": API_KEY
    }

    response = requests.get(url, headers=headers, timeout = 10)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    balance = get_eth_balance(ADDRESS)
    print("Wallet balance:")
    print(balance)