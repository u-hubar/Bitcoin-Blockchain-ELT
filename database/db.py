import logging
import sys

import pandas as pd
import psycopg2
import psycopg2.extras
from utils import config
from utils.decorators import use_cursor

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(name)s - %(message)s"
)
logger = logging.getLogger("Blockchain-ETL-Database")


class Database:
    def __init__(self):
        self.connection = self._connect()

    def select_unexplored_entities(self):
        select_query = """
            SELECT e.address, a.txhash
            FROM Blockchain.Entities e
            INNER JOIN Blockchain.Addresses a
            ON e.address = a.address
            WHERE a.entity IS NULL
        """

        unexplored_entities = pd.read_sql_query(
            select_query,
            self.connection
        )

        return unexplored_entities

    @use_cursor
    def update_addresses_entities(self, entities, cursor):
        update_query = """
            UPDATE Blockchain.Addresses
            SET entity = %s
            WHERE address = %s
        """

        psycopg2.extras.execute_batch(
            cursor,
            update_query,
            entities
        )

    @use_cursor
    def select_entity_by_address(self, address, cursor):
        select_query = """
            SELECT entity
            FROM Blockchain.Addresses
            WHERE address = %s
        """

        cursor.execute(select_query, (address,))

    @use_cursor
    def select_addreses_by_entity(self, entity, cursor):
        select_query = """
            SELECT address
            FROM Blockchain.Addresses
            WHERE entity = %s
        """

        cursor.execute(select_query, (entity,))

    @use_cursor
    def insert_transactions(self, transactions, cursor):
        insert_query = """
            INSERT INTO Blockchain.Transactions (txhash, timestamp, blockhash, ip, hasScript, unspent)
            VALUES(%s, %s, %s, %s, %s, %s)
        """

        psycopg2.extras.execute_batch(cursor, insert_query, transactions)

    @use_cursor
    def insert_addresses(self, addreses, cursor):
        insert_query = """
            INSERT INTO Blockchain.Addresses (address, tag, balance, isMiner, entity)
            VALUES(%s, %s, %s, %s, %s)
        """

        psycopg2.extras.execute_batch(cursor, insert_query, addreses)

    @use_cursor
    def insert_input_sections(self, inputs, cursor):
        insert_query = """
            INSERT INTO Blockchain.inputSection (txhash, address, amount)
            VALUES(%s, %s, %s)
        """

        psycopg2.extras.execute_batch(cursor, insert_query, inputs)

    @use_cursor
    def insert_output_sections(self, outputs, cursor):
        insert_query = """
            INSERT INTO Blockchain.outputSection (txhash, address, amount, isMining)
            VALUES(%s, %s, %s, %s)
        """

        psycopg2.extras.execute_batch(cursor, insert_query, outputs)

    @use_cursor
    def insert_entities(self, entities, cursor):
        insert_query = """
            INSERT INTO Blockchain.Entities (txhash, address)
            VALUES(%s, %s)
        """

        psycopg2.extras.execute_batch(cursor, insert_query, entities)

    def _connect(self):
        logger.info("Connecting to PG Database...")
        connection = psycopg2.connect(
            dbname=config.PG_DBNAME,
            user=config.PG_USR,
            password=config.PG_PSWD,
            host=config.PG_HOST,
            port=config.PG_PORT,
        )
        logger.info("Successfully connected to PG Database!")

        connection.autocommit = True

        return connection


if __name__ == "__main__":
    df = Database()
