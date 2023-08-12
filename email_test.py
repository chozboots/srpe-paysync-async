import asyncio
from database import Queries
from database import UnionDatabase
import logging

user_database = UnionDatabase()
query_executor = Queries(user_database)

logging.basicConfig(
    filename=None,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

logger = logging.getLogger(__name__)

# This is a coroutine and must be awaited
async def test_email_query():
    await user_database.create_pool()
    email = 'example@test.com'
    user = await query_executor.get_user_by_email(email)
    logger.debug(f"Checking if email '{email}' exists: {bool(user)}")
    await user_database.close_pool()  # Clean up after testing

# Run the coroutine using asyncio
asyncio.run(test_email_query())
