import requests
import logging
import json
import etl.utils.config as config

logger = logging.getLogger("Blockchain-ETL")


class Block:
    def __init__(self, hash):
        self.hash = hash
        # self.input_section = self._parse_input_section()
        self.output_section = self._parse_output_section()

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
    
    def _parse_output_section(self):
        try:
            response = requests.get(config.SINGLE_BLOCK_URL.format(self.hash))

        except Exception as err:
            logger.error(err)

        assert response.status_code == 200, "Failed single block GET request!"

        block = response.json()

        output_section = []

        for txn in block["tx"]:
            
            for out in txn["out"]:
                if not out["spent"]:
                    continue

                if out['addr'] == '12dRugNcdxK39288NjcDV4GX7rMsKCGn6B':
                    is_miner = True
                    print("+")
                else:
                    is_miner = False

                txn_hash = txn["hash"]
                out_addr = out["addr"]
                out_value = out["value"]

                output_section.append((txn_hash, out_addr, out_value, is_miner))

        return output_section

block = Block('000000000000000000116c752256d0bb80a9a4c3efa2fd520aa2cfcb388bbde2')