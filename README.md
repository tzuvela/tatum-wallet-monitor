# Tatum Wallet Monitor

Short Python utility that queries the Tatum Data API to monitor an Ethereum wallet and export recent transaction history to CSV for record-keeping.

## Technology Used

- API provider: Tatum
- Blockchain: Ethereum (Sepolia testnet by default)

## How to run

1. Create and activate a virtual environment
2. Install dependencies:
   pip install -r requirements.txt
3. Configure environment variables (see below)
4. Run the script:
   python main.py

## Configuration

This project uses environment variables to avoid hard-coding secrets and to make the script easy to reuse across environments.

Copy the example file:
cp .env.dist .env

Fill in the required values:

- TATUM_API_KEY – your Tatum API key
- CHAIN – blockchain network to query  
  Allowed values for this demo:
  - sepolia (default, recommended)
  - ethereum
- WALLET_ADDRESS – Ethereum-compatible wallet address

## Output

- Recent transactions are printed to the console
- Transaction history is exported to transactions.csv for record-keeping

## Current limitations

- Requests can time out
- Transaction list may include fees or internal transfers
- Output formatting is still a work in progress

## Relevant Tatum API Endpoints

This project uses the following Tatum APIs:

- Ethereum balance (v3):  
  https://apidoc.tatum.io/tag/Ethereum#operation/EthGetBalance

- Transaction history (v4 Data API):  
  https://apidoc.tatum.io/tag/Data#operation/GetTransactions
