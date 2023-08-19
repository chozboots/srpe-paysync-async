# standard
import logging
from typing import TYPE_CHECKING

# local
from database.formatters import User, Login_Info
from errorHandlers.database import query_error


if TYPE_CHECKING:
    from database import UnionDatabase

logger = logging.getLogger(__name__)

class Queries:
    def __init__(self, db: 'UnionDatabase'):
        self.db = db
        
    # -------------------
    # User related queries
    # -------------------
    @query_error
    async def insert_user(self, user: User) -> int:
        query = """
            INSERT INTO users (email, first_name, last_name, phone, address1, address2, city, state, zip_code) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING user_id
            """
        result = await self.db.fetch(query, user.email, user.first_name, user.last_name, user.phone, user.address1, user.address2, user.city, user.state, user.zip_code)
        return result[0]['user_id'] if result else None

    @query_error
    async def get_user_by_email(self, email: str) -> int:
        query = """SELECT user_id FROM users WHERE email = $1"""
        result = await self.db.fetch(query, email)
        return result[0]['user_id'] if result and len(result) > 0 else None

    @query_error
    async def get_user_by_phone(self, phone: int) -> int:
        query = """SELECT user_id FROM users WHERE phone = $1"""
        result = await self.db.fetch(query, phone)
        return result[0]['user_id'] if result and len(result) > 0 else None

    @query_error
    async def get_profile_info(self, user_id: int) -> dict:
        query = """SELECT * FROM users WHERE user_id = $1"""
        result = await self.db.fetch(query, user_id)
        return result[0] if result and len(result) > 0 else None
    
    @query_error
    async def update_user_customer_id(self, user_id: int, customer_id: str):
        query = """UPDATE users SET customer_id = $1 WHERE user_id = $2"""
        await self.db.execute(query, customer_id, user_id)

    # -----------------------------
    # Stripe general info related queries
    # -----------------------------
    @query_error
    async def insert_stripe_general_info(self, user_id: int, customer_id: str, payment_method: str = None, last4: str = None, expiration = None, has_funds: bool = False):
        query = """
               INSERT INTO stripe_general_info (customer_id, user_id, payment_method, last4, expiration, has_funds)
               VALUES ($1, $2, $3, $4, $5, $6)
               """
        await self.db.execute(query, customer_id, user_id, payment_method, last4, expiration, has_funds)

    @query_error
    async def get_stripe_general_info(self, user_id: int) -> dict:
        query = """SELECT * FROM stripe_general_info WHERE user_id = $1"""
        result = await self.db.fetch(query, user_id)
        return result[0] if result and len(result) > 0 else None

    @query_error
    async def get_customer_id_by_user_id(self, user_id: int) -> str:
        query = """SELECT customer_id FROM users WHERE user_id = $1"""
        result = await self.db.fetch(query, user_id)
        return result[0]['customer_id'] if result and len(result) > 0 else None

    # -------------------
    # Login related queries
    # -------------------
    @query_error
    async def insert_login(self, login: Login_Info):
        query = """INSERT INTO login_info (user_id, password_hash) 
                   VALUES ($1, $2)"""
        await self.db.execute(query, login.user_id, login.password_hash)

    @query_error
    async def get_login_info(self, user_id: int) -> dict:
        query = """SELECT * FROM login_info WHERE user_id = $1"""
        result = await self.db.fetch(query, user_id)
        return result[0] if result and len(result) > 0 else None
