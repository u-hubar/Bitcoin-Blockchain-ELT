import logging
import time

import requests
from etl.utils import config

logger = logging.getLogger("Blockchain-ETL")


class Block:
    def __init__(self, hash):
        self.hash = hash
        self.input_section = self._parse_input_section()
        self.output_section = self._parse_output_section()
        #self.transactions = self._parse_transaction()
        self.addresses = self._parse_addresses()

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
    
    def _parse_addresses(self):
        addresses = []
        
        for addr in self.output_section:
            time.sleep(2)
            try:
                response = requests.get(f"https://blockchain.info/multiaddr?active={addr[1]}")
            except Exception as err:
                logger.error(err)
                continue

            assert response.status_code == 200, f"Failed single address GET request! (Response {response.status_code})"

            address_all = response.json()
            ad = address_all['addresses']
            address = ad[0]
            add = address["address"]
            balance = address["final_balance"]
            print(balance)
            is_miner = False
            for tr in address_all['txs']:
                for inp in tr["inputs"]:
                    if inp["prev_out"] is None:
                        is_miner = True
            print(f"addr = {add},balance = {balance},miner = {is_miner}")
            addresses.append((add,balance,is_miner))   

        for addr in self.input_section:
            time.sleep(2)
            try:
                response = requests.get(f"https://blockchain.info/multiaddr?active={addr[1]}")
            except Exception as err:
                logger.error(err)
                continue

            assert response.status_code == 200, f"Failed single address GET request! (Response {response.status_code})"

            address_all = response.json()
            ad = address_all['addresses']
            address = ad[0]
            add = address["address"]
            balance = address["final_balance"]
            is_miner = False
            for tr in address_all['txs']:
                for inp in tr["inputs"]:
                    if inp["prev_out"] is None:
                        is_miner = True
            print(f"addr = {add},balance = {balance},miner = {is_miner}")
            addresses.append((add,balance,is_miner))   

        # print(address)   
        return addresses

            


block = Block('0000000000000000000aa1c83f77d1bb70a7a5508cb1cabcbea21a002addf07e')
