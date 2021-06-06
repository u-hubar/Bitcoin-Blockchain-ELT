import requests
import logging
import json
import etl.utils.config as config
import time

logger = logging.getLogger("Blockchain-ETL")


class Block:
    def __init__(self, hash):
        self.hash = hash
        self.input_section = self._parse_input_section()
        #self.output_section = self._parse_output_section()
        #self.transactions = self._parse_transaction()
        self.addresses = self._parse_addreses()

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
                else:
                    is_miner = False

                txn_hash = txn["hash"]
                out_addr = out["addr"]
                out_value = out["value"]


                output_section.append((txn_hash, out_addr, out_value, is_miner))

        return output_section
    
    def _parse_transaction(self):
        try:
            response = requests.get(config.SINGLE_BLOCK_URL.format(self.hash))

        except Exception as err:
            logger.error(err)

        assert response.status_code == 200, "Failed single block GET request!"

        block = response.json()

        block_hash = block['hash']
        time = block['time']
        
        transactions =[]

        for txn in block["tx"]:
            trans_ip = txn['relayed_by']
            trans_hash = txn['hash']
            for inp in txn['inputs']:
                try:
                    has_script = True if inp["script"] else False
                except KeyError:
                    pass
            unspent = txn['double_spend']
        
            transactions.append((trans_hash,time,block_hash,trans_ip,has_script,unspent))

        return transactions
    
    def _parse_addreses(self):
        addresses = []

        for addr in self.input_section:
            try:
                response = requests.get(config.SINGLE_ADDRESS_URL.format(addr))
            except Exception as err:
                continue
            address = response.json()
            print(address)
            balance = address["final_balance"]
            addresses.append(addr,balance)            

            


block = Block('000000000000000000116c752256d0bb80a9a4c3efa2fd520aa2cfcb388bbde2')