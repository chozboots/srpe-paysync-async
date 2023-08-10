# standard
import os
import logging

# third-party
import asyncpg

# dev
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


logger = logging.getLogger(__name__)

class UnionDatabase:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        self.pool = None

    async def create_pool(self):
        try:
            self.pool = await asyncpg.create_pool(self.database_url)
            logger.info('Database connection pool created')
        except Exception as e:
            logger.error(f"Database connection pool creation failed: {e}")
            raise

    async def close_pool(self):
        await self.pool.close()
        logger.info('Database connection pool closed')

    async def execute_query(self, query, *params):
        try:
            async with self.pool.acquire() as connection:
                connection: asyncpg.Connection # type hint
                return await connection.fetch(query, *params)
        except Exception as e:
            logger.error(f"An error occurred when trying to execute query: {e}")
            raise
