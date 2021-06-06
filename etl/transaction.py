import requests
import logging
import json
import etl.utils.config as config

logger = logging.getLogger("Blockchain-ETL")


class Block:
    def __init__(self, hash):
        self.hash = hash
        self.transaction = transaction()

    def transaction(self):
        try:
            response = requests.get(config.SINGLE_TRANSACTION_URL.format(self.hash))

        except Exception as err:
            logger.error(err)

        assert response.status_code == 200, "Failed single transaction GET request!"

        transaction = response.json()
        print(transaction[1])