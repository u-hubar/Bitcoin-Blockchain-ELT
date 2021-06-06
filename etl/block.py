import requests
import logging

from utils import config

logger = logging.getLogger("Blockchain-Warehouse")


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
            txn_hash = txn["hash"]
            for inp in txn["inputs"]:

                if inp["prev_out"] is None:
                    continue

                inp_addr = inp["prev_out"]["addr"]
                inp_value = inp["prev_out"]["value"]

                input_section.append((txn_hash, inp_addr, inp_value))

        return input_section
