import logging
import sys

from database.db import Database

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(name)s - %(message)s"
)
logger = logging.getLogger("Blockchain-Warehouse")


class BlocksTransformer(Database):
    def __init__(self):
        super(Database, self).__init__()
        self.i_entities = self.select_inexplored_entities()
        self.i_transactions = []
        self.i_addresses = []
        self.e_entities = []
        self.e_transactions = []
        self.e_addreses = []

    def clasterize(self):
        index = self.select_last_entity()
        index = 1 if index is None else index + 1

        while self.i_entities:
            self.e_addreses = []
            self.e_transactions = []
            self.i_addresses = []
            self.i_transactions = []

            while self.i_addresses and self.i_transactions:
                self.find_inexplored_addresses()
                self.find_inexplored_transactions()

            self.remove_explored_entities()
            self.update_entities()
            self.update_addresses_entities(
                [(index, addr) for addr in self.e_addreses]
            )

    def find_inexplored_transactions(self):
        if self.i_addresses:
            addr = self.i_addresses.pop(0)

            addr_transactions = self.i_entities.loc[
                self.i_entities["address"] == addr, "txhash"
            ].tolist()
            inexplored = list(
                set(addr_transactions) - set(self.e_transactions)
            )

            self.i_transactions.extend(inexplored)
            self.e_addreses.append(addr)

    def find_inexplored_addresses(self):
        if self.i_transactions:
            tx = self.i_transactions.pop(0)

            tx_addresses = self.i_entities.loc[
                self.i_entities["txhash"] == tx, "address"
            ].tolist()
            inexplored = list(set(tx_addresses) - set(self.e_addreses))

            self.i_addresses.extend(inexplored)
            self.e_transactions.append(tx)

    def remove_explored_entities(self):
        self.i_entities = self.i_entities[
            ~self.i_entities.isin(self.e_transactions)
        ]

    def update_entities(self):
        for addr in self.e_addreses:
            addr_entity = self.select_entity_by_address(addr)

            if addr_entity is not None:
                entity_addresses = self.select_addreses_by_entity(addr_entity)

                explored = set(entity_addresses - set(self.e_addreses))
                self.e_addreses.extend(explored)
