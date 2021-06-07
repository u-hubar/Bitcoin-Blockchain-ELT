import argparse
import logging
import sys

from etl.blocks_extractor import BlocksExtractor
from etl.blocks_transformer import BlocksTransformer

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(name)s - %(message)s"
)
logger = logging.getLogger("Blockchain-Warehouse")


def parse_args():
    description = """Bitcoin Blockchain Warehouse"""
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=formatter_class, description=description
    )
    parser.add_argument(
        "--year",
        "-Y",
        metavar="YEAR",
        required=True,
        type=int,
        help="INT: Year of blocks to explore",
    )
    parser.add_argument(
        "--month",
        "-M",
        metavar="MONTH",
        required=True,
        type=int,
        help="INT: Month of blocks to explore",
    )
    parser.add_argument(
        "--day",
        "-D",
        metavar="DAY",
        required=True,
        type=int,
        help="INT: Day of blocks to explore",
    )
    parser.add_argument(
        "--limit",
        "-L",
        metavar="LIMIT",
        required=True,
        type=int,
        help="INT: Maximum number of blocks to explore",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="FLAG: Print debug messages",
    )

    args = parser.parse_args()
    setattr(args, "prog", parser.prog)
    return args


def setup_logging(debug):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def main(args):
    blocks_extractor = BlocksExtractor(
        args.year, args.month, args.day, args.limit
    )
    blocks_transformer = BlocksTransformer()

    blocks_extractor.load_blocks()
    blocks_transformer.clasterize()


if __name__ == "__main__":
    args = parse_args()
    setup_logging(args.debug)

    main(args)
