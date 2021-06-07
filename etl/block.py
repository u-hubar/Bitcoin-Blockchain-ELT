import logging
from datetime import datetime
from utils.decorators import exponential_backoff

import pandas as pd
import requests
from tqdm import tqdm
from utils import config

logger = logging.getLogger("Blockchain-ETL")


class Block:
    def __init__(self, hash):
        self.hash = hash
        self._parse_block()
        self._save_parsed_block()

    def _parse_block(self):
        block_info = self._get_block()

        self.transactions = []
        self.addresses = []
        self.input_section = []
        self.output_section = []

        # Iterating over block transactions
        tx_pbar = tqdm(block_info["tx"], total=len(block_info["tx"]))
        for txn in tx_pbar:
            tx_pbar.set_description(
                desc=f"Transaction {len(self.transactions)} / {len(block_info['tx'])}"
            )

            is_miner = False
            txn_hash = txn["hash"]

            txn_info = self._get_transaction(txn_hash)

            # Continue if transaction request failed
            if txn_info is None:
                continue

            txn_time = datetime.utcfromtimestamp(int(txn_info["time"]))
            txn_ip = txn_info["relayed_by"]

            # Appending single transaction information
            self.transactions.append((txn_hash, txn_time, self.hash, txn_ip))

            for inp in txn_info["inputs"]:
                if inp["prev_out"] is None:
                    is_miner = True
                    continue

                inp_addr = inp["prev_out"]["addr"]
                inp_amount = inp["prev_out"]["value"]

                inp_has_script = False
                try:
                    if inp["script"]:
                        inp_has_script = True

                except KeyError:
                    pass

                # Appending single transaction input section information
                self.input_section.append(
                    (txn_hash, inp_addr, inp_amount, inp_has_script)
                )

                # Appending single transacction input address information
                if not any([addr[0] == inp_addr for addr in self.addresses]):
                    balance_info = self._get_balance(inp_addr)
                    # Continue if balance request failed
                    if balance_info is None:
                        continue

                    addr_balance = balance_info[inp_addr]["final_balance"]
                    self.addresses.append((inp_addr, addr_balance))

            for out in txn_info["out"]:
                if "addr" not in out.keys():
                    continue

                out_addr = out["addr"]
                out_amount = out["value"]
                out_unspent = not out["spent"]

                # Appending single transaction output section information
                self.output_section.append(
                    (txn_hash, out_addr, out_amount, out_unspent, is_miner)
                )

                # Appending single transaction output address information
                if not any([addr[0] == out_addr for addr in self.addresses]):
                    balance_info = self._get_balance(out_addr)
                    # Continue if balance request failed
                    if balance_info is None:
                        continue

                    addr_balance = balance_info[out_addr]["final_balance"]
                    self.addresses.append((out_addr, addr_balance))

    @exponential_backoff(logger, retries=3, backoff=1, delay=0.1)
    def _get_block(self):
        try:
            response = requests.get(config.SINGLE_BLOCK_URL.format(self.hash))

        except Exception as err:
            logger.error(err)

        if response.status_code != 200:
            return None

        block_info = response.json()

        return block_info

    @exponential_backoff(logger, retries=3, backoff=1, delay=0.1)
    def _get_transaction(self, txn_hash):
        try:
            response = requests.get(
                config.SINGLE_TRANSACTION_URL.format(txn_hash)
            )

        except Exception as err:
            logger.error(err)

        if response.status_code != 200:
            return None

        txn_info = response.json()

        return txn_info

    @exponential_backoff(logger, retries=3, backoff=1, delay=0.1)
    def _get_balance(self, addr):
        try:
            response = requests.get(config.SINGLE_BALANCE_URL.format(addr))

        except Exception as err:
            logger.error(err)

        if response.status_code != 200:
            return None

        addr_info = response.json()

        return addr_info

    def _save_parsed_block(self):
        transactions_df = pd.DataFrame(
            self.transactions,
            columns=["txhash", "timestamp", "blockhash", "ip"],
        )
        addreses_df = pd.DataFrame(
            self.addresses, columns=["address", "balance", "isMiner"]
        )
        inputs_df = pd.DataFrame(
            self.output_section,
            columns=["txhash", "address", "amount", "hasScript"],
        )
        outputs_df = pd.DataFrame(
            self.input_section,
            columns=["txhash", "address", "amount", "unspent", "isMining"],
        )

        transactions_df.to_csv("data/transactions.tsv", sep="\t", index=False)
        addreses_df.to_csv("data/addresses.tsv", sep="\t", index=False)
        inputs_df.to_csv("data/inputs.tsv", sep="\t", index=False)
        outputs_df.to_csv("data/outputs.tsv", sep="\t", index=False)


block = Block(
    "0000000000000000000aa1c83f77d1bb70a7a5508cb1cabcbea21a002addf07e"
)
