# standard
import logging

# third-party
import asyncpg


logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Base class for database-related errors"""

class InsertionError(DatabaseError):
    def __init__(self, message, constraint_name, field_name):
        super().__init__(message)
        self.constraint_name = constraint_name
        self.field_name = field_name

class DeletionError(DatabaseError):
    """Raised when there's an error deleting data from the database"""

def query_error(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        
        # Handle unique constraint violations
        except asyncpg.UniqueViolationError as e:
            logger.error(f"(databaseEH) UniqueViolationError: constraint_name={e.constraint_name}, detail={e.detail}, error={str(e)}")
            message = f"(databaseEH) A {e.__class__.__name__} occurred when trying to execute {func.__name__}."
            raise InsertionError(message, e.constraint_name, str(e).split(' ')[-1])
        
        # Handle invalid data passed in query
        except asyncpg.DataError:
            logger.error(f"(databaseEH) A DataError occurred when trying to execute {func.__name__}.")
            raise DatabaseError(f"(databaseEH) Error: Invalid data used in query.")
        
        # Handle connection-related errors
        except asyncpg.InterfaceError:
            logger.error(f"(databaseEH) An InterfaceError occurred when trying to execute {func.__name__}.")
            raise DatabaseError(f"(databaseEH) Error: Unable to establish a database connection.")
        
        # General error handling
        except Exception as e:
            logger.error(f"(databaseEH) An unexpected error occurred when trying to execute {func.__name__}. Error: {e.__class__.__name__}")
            raise DatabaseError(f"(databaseEH) Error: An unexpected error occurred during query execution.")
    
    return wrapper
