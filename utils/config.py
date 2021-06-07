import os


# URLS
BLOCKS_URL = "https://blockchain.info/blocks/{}?format=json"
SINGLE_BLOCK_URL = "https://blockchain.info/rawblock/{}"
SINGLE_TRANSACTION_URL = "https://blockchain.info/rawtx/{}"
SINGLE_BALANCE_URL = "https://blockchain.info/balance?active={}"

# PostgreSQL
PG_DBNAME = "blockchain"
PG_USR = "postgres"
PG_PSWD = os.environ["PG_PSWD"]
PG_HOST = "192.168.0.105"
PG_PORT = "5432"
