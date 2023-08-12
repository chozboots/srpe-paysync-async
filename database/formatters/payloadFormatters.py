# standard
from datetime import datetime
import logging

# local
from database.utils import hash_password

# third-party
import pytz


logger = logging.getLogger(__name__)

def format_value(value, key=None) -> str:
    if isinstance(value, str):
        if "@" in value:  # email
            return value.lower()
        elif " " in value:  # address
            return value.title()
        elif key == 'state':  # state
            return value.upper()
        else:
            return value.title()  # name
    else:
        return value

logger = logging.getLogger(__name__)

async def _get_time(data: dict):
    try:
        cst_tz = pytz.timezone('America/Chicago')
        if data.get('registered'):
            registered = data['registered']
        else:
            registered = datetime.now(cst_tz)
    except pytz.UnknownTimeZoneError as e:
        logger.error("Unknown timezone encountered while creating user.")
        registered = None
        raise e
    except Exception as e:
        logger.error("An error occurred while setting registered time.")
        registered = None
        raise e
    return registered

class User:
    def __init__(self, data: dict):
        self.email = format_value(data['email'])
        self.first_name = format_value(data['first_name'])
        self.last_name = format_value(data['last_name'])
        self.phone = format_value(data['phone'])
        self.address1 = format_value(data['address1'])
        self.address2 = format_value(data.get('address2', None))
        self.city = format_value(data['city'])
        self.state = format_value(data['state'], 'state')
        self.zip_code = format_value(data['zip_code'])
        self.registered = _get_time(data)
            
class Login_Info:
    def __init__(self, user_id: int, password: str):
        self.password_hash = hash_password(password)
        self.user_id = user_id # FK from users
        
class Stripe_General_Info:
    def __init__(self, user_id: int, customer_id: str):
        self.user_id = user_id
        self.customer_id = customer_id
        
        self.payment_method = None
        self.last4 = None
        self.expiration = None # null if not card
        self.has_funds = None # null if not applicable, bool otherwise

class Stripe_Session_Info:
    def __init__(self, user_id: int, customer_id: str):
        self.user_id = user_id # FK from users
        self.customer_id = customer_id
        
        self.token = None 
        # allows access to links from dashboard, uses jwt tokens
        self.checkout_status = None
        self.checkout_link = None
        self.checkout_link_expires = None # expiration date
        self.payment_status = None # mainly used for micro-deposit tracking
        
        
        
