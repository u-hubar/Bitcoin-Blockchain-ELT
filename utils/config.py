import os

# URLS
BLOCKS_URL = "https://blockchain.info/blocks/{}?format=json"
SINGLE_BLOCK_URL = "https://blockchain.info/rawblock/{}"
SINGLE_ADDRESS_URL = "https://blockchain.info/rawaddr/{}"

# PostgreSQL
PG_DBNAME = "blockchain"
PG_USR = "postgres"
PG_PSWD = os.environ["PG_PSWD"]
PG_HOST = "192.168.0.105"
PG_PORT = "5432"
