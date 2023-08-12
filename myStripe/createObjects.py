# standard
import os

# third-party
import stripe

# local
from errorHandlers.stripe import object_error
from database.formatters import User

# dev
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


success_url = os.environ.get('SUCCESS_URL')

@object_error
async def create_customer(user: User):
    return await stripe.Customer.create(
        name=', '.join([user.last_name, user.first_name]),
        email=user.email,
        phone=user.phone,
        address={
            'line1': user.address1,
            'line2': user.address2,
            'city': user.city,
            'state': user.state,
            'postal_code': user.zip_code
        }
    )

@object_error
async def create_session(customer: stripe.Customer):
    return await stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=['us_bank_account'],
        mode='setup',
        success_url=success_url,
    )