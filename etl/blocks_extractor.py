import datetime
import logging
import sys

import requests
from database.db import Database
from tqdm import tqdm
from utils import config

from etl.block import Block

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(name)s - %(message)s"
)
logger = logging.getLogger("Blockchain-Warehouse")


class BlocksExtractor(Database):
    def __init__(self, year, month, day, blocks_limit=5):
        super(Database, self).__init__()
        self.blocks_limit = blocks_limit
        self.hashes = self._load_hashes(year, month, day)

    def load_blocks(self):
        blocks_pbar = tqdm(self.hashes, total=len(self.hashes))
        for i, hash in enumerate(blocks_pbar):
            blocks_pbar.set_description(
                desc=f"Block {i} / {len(self.hashes)}"
            )
            block = Block(hash)

            self.insert_addresses(block.addresses)
            self.insert_transactions(block.transactions)
            self.insert_input_sections(block.input_sections)
            self.insert_output_sections(block.output_sections)

    def _load_hashes(self, year, month, day):
        epoch = (
            datetime.datetime(year, month, day, 0, 0).strftime("%s") + "000"
        )
        try:
            response = requests.get(config.BLOCKS_URL.format(epoch))

        except Exception as err:
            logger.error(err)

        assert response.status_code == 200, "Failed blocks GET request!"

        blocks = response.json()
        hashes = [b["hash"] for b in blocks]

        return hashes[:self.blocks_limit]
