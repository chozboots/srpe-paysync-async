from errorHandlers.stripe import webhook_error
from stripe import PaymentMethod, Customer
import logging

logger = logging.getLogger(__name__)

@webhook_error
async def checkout_completed(event):
    try:
        # Log the full event object for debugging
        logger.info(f"Received event: {event}")

        session = event['data']['object']
        logger.info(f"Checkout session completed for customer: {session['customer']}")

        has_payment_method = False
        for _ in range(5):
            payment_methods = PaymentMethod.list(
                customer=session['customer'],
                type='us_bank_account',
            )
            if payment_methods['data']:
                payment_method = payment_methods['data'][0]

                if 'bank_account' in payment_method:
                    verification_method = payment_method['bank_account']['verification_method']
                    logger.info(f"  Verification method: {verification_method}")

                logger.info(f"Setting default payment method to: {payment_method.id}")

                Customer.modify(
                    session['customer'],
                    invoice_settings={
                        'default_payment_method': payment_method.id,
                    },
                )

                has_payment_method = True

                logger.info("Default payment method set successfully.")
                break

        if not has_payment_method:
            logger.error('Could not detect payment method.')

    except Exception as e:
        # Log any exceptions that occur during event handling
        logger.error(f"Error handling checkout completed event: {e}")
        