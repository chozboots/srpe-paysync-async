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

    async def create_pool(self, min_size=10, max_size=100):
        """Create a database connection pool."""
        try:
            self.pool = await asyncpg.create_pool(self.database_url, min_size=min_size, max_size=max_size)
            logger.info('Database connection pool created')
        except Exception as e:
            logger.error(f"Database connection pool creation failed: {e}")
            raise

    async def close_pool(self):
        """Close the database connection pool."""
        await self.pool.close()
        logger.info('Database connection pool closed')

    async def execute(self, query, *params) -> None:
        """Execute a DML statement."""
        if not self.pool:
            raise Exception("Connection pool not initialized. Call create_pool() first.")
        
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(query, *params)
        except Exception as e:
            logger.error(f"An error occurred when trying to execute DML: {e}")
            raise

    async def fetch(self, query, *params) -> list:
        """Execute a DQL statement and return results."""
        if not self.pool:
            raise Exception("Connection pool not initialized. Call create_pool() first.")
        
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetch(query, *params)
        except Exception as e:
            logger.error(f"An error occurred when trying to execute DQL: {e}")
            raise

# Example usage (when required):
# db = UnionDatabase()
# await db.create_pool()
# results = await db.fetch("SELECT * FROM users WHERE email=$1", "test@example.com")
# await db.close_pool()
