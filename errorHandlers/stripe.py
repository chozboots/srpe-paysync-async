# standard
from functools import wraps
import logging

# third-party
import stripe
from stripe import error as stripe_error


logger = logging.getLogger(__name__)

def object_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            if isinstance(result, stripe.Customer):
                logger.info("Stripe customer created with ID: " + result.id)
            elif isinstance(result, stripe.checkout.Session):
                logger.info("Checkout session created with ID: " + result.id)

            return result

        except stripe_error.RateLimitError as e:
            logger.error(f"Too many requests made to API: {e}")
            raise
        except stripe_error.InvalidRequestError as e:
            logger.error(f"Entry/entries are missing or of an improper format: {e}")
            raise
        except stripe_error.AuthenticationError as e:
            logger.error(f"Could not authenticate; check API key: {e}")
            raise
        except stripe_error.APIConnectionError as e:
            logger.error(f"Network failure: {e}")
            raise
        except stripe_error.StripeError as e:
            logger.error(f"Unhandled error occurred; act immediately: {e}")
            raise
        except Exception as e:
            logger.error(f"Error unrelated to Stripe occurred; refer to traceback: {e}")
            raise
    return wrapper

def webhook_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            event = await func(*args, **kwargs)
            return event
        except ValueError as e:
            logger.error(f"Invalid payload received in webhook: {e}")
            return 'Invalid payload', 400
        except stripe_error.SignatureVerificationError as e:
            logger.error(f"Invalid signature received in webhook: {e}")
            return 'Invalid signature', 400
        except Exception as e:
            logger.error(f"Unexpected error occurred in webhook: {e}")
            raise
    return wrapper

