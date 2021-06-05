import requests
import logging
import sys
import datetime

from etl.block import Block
import etl.utils.config as config

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(name)s - %(message)s"
)
logger = logging.getLogger("Blockchain-ETL")


class BlocksExtractor:
    def __init__(self, year, month, day):
        self.hashes = self._load_hashes(year, month, day)

    def load_inputs(self):
        all_input_section = []
        for hash in self.hashes:
            block = Block(hash)
            all_input_section.extend(block.input_section)
            
        return all_input_section

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

        return hashes

block = BlocksExtractor(2020,4,15) 
print(block.hashes[1])
