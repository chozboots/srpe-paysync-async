import logging
import asyncio

from database import UnionDatabase
from database import Queries


# setup logging
logging.basicConfig(
    filename='unionDatabase.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

logger = logging.getLogger(__name__)

# Create UnionDatabase and Queries instances
db = UnionDatabase()
queries = Queries(db)

# Test functions
async def test_query(table_name: str):
    query = f"SELECT * FROM {table_name} LIMIT 5;"
    try:
        await queries.execute_query(query)
        logger.debug(f'Query in table [{table_name}] executed successfully.')
    except Exception as e:
        logger.error(f"An error ({e}) occurred connected to table [{table_name}]")

async def test_db_connection(*table_names):
    for name in table_names:
        try:
            await test_query(name)
        except Exception as e:
            logger.error(f'Error running test query on table [{name}]: {e}')

# Main function
async def main():
    await db.create_pool()
    await test_db_connection('users')
    await asyncio.sleep(10)
    await db.close_pool()

# Run main function if this is the main script being run
if __name__ == "__main__":
    asyncio.run(main())
