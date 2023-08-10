# standard
import logging

# third-party
import bcrypt


logger = logging.getLogger(__name__)

def hash_password(password: str):
    # password string from form
    password = password.encode('utf-8')

    # generate a salt and hash the password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    # password_hash value, decoded to a string
    return hashed.decode('utf-8')

def check_password(password: str, hashed: str):
    # correct
    if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
        return True
    # incorrect
    else:
        return False
