import requests
import logging

import etl.utils.config as config

logger = logging.getLogger("Blockchain-ETL")


class Block:
    def __init__(self, hash):
        self.hash = hash
        self.input_section = self._parse_input_section()

    def _parse_input_section(self):
        try:
            response = requests.get(config.SINGLE_BLOCK_URL.format(self.hash))

        except Exception as err:
            logger.error(err)

        assert response.status_code == 200, "Failed single block GET request!"

        block = response.json()

        input_section = []
        for txn in block["tx"]:
            for inp in txn["inputs"]:

                if inp["prev_out"] is None:
                    continue

                txn_hash = txn["hash"]
                inp_addr = inp["prev_out"]["addr"]
                inp_value = inp["prev_out"]["value"]

                input_section.append((txn_hash, inp_addr, inp_value))

        return input_section
