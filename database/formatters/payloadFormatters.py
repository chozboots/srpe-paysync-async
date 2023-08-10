# local
from database.utils import hash_password


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

class Login:
    def __init__(self, password: str, user_id: int):
        self.password_hash = hash_password(password)
        self.user_id = user_id

