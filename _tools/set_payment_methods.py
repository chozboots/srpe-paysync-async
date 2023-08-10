# standard
import os

# third-party
import stripe

# dev
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# secret key
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# get the list of customers
customers = stripe.Customer.list()

for customer in customers.auto_paging_iter():
    print(f"Customer ID: {customer.id}")
    
    # get the list of payment methods for each customer
    payment_methods = stripe.PaymentMethod.list(
        customer=customer.id,
        type='us_bank_account',
    )
    
    # check if the customer has any payment methods
    if len(payment_methods['data']) > 0:
        print(f"Customer {customer.id} has {len(payment_methods['data'])} payment method(s):")
        
        for payment_method in payment_methods['data']:
            print(f"  Payment method ID: {payment_method.id}")
            
            # update the customer to set the default payment method
            stripe.Customer.modify(
                customer.id,
                invoice_settings={
                    'default_payment_method': payment_method.id,
                },
            )
            
            print(f"  Default payment method for {customer.id} set to {payment_method.id}.")
            
    else:
        print(f"Customer {customer.id} has no payment methods.")
    
    print("\n")
