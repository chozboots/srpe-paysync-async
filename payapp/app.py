# standard
import os
import logging
from urllib.parse import urlparse
from datetime import timedelta

# third-party
from quart import Quart, redirect, url_for
from quart_jwt_extended import JWTManager
from quart_cors import cors
from quart_rate_limiter import RateLimiter
from quart_rate_limiter.redis_store import RedisStore
import stripe

# local
from database import UnionDatabase  # loads PostgreSQL database
from routes import dashboard_bp # dashboard blueprint
from routes import signup_bp # signup blueprint

# dev
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


logger = logging.getLogger(__name__)

# envs
try:
    # stripe
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    if stripe.api_key:
        logger.info("STRIPE_SECRET_KEY loaded successfully.")
    else:
        logger.error("Failed to load STRIPE_SECRET_KEY.")

    # webhook
    endpoint_secret = os.environ.get('WEBHOOK_SIGNING_SECRET')
    if endpoint_secret:
        logger.info("WEBHOOK_SIGNING_SECRET loaded successfully.")
    else:
        logger.error("Failed to load WEBHOOK_SIGNING_SECRET.")
        
    # success
    success_url = os.environ.get('SUCCESS_URL')
    if success_url:
        # Check if success_url is valid
        try:
            result = urlparse(success_url)
            # A valid URL will at least have a scheme and netloc
            if all([result.scheme, result.netloc]):
                logger.info("SUCCESS_URL loaded and valid.")
            else:
                logger.error("SUCCESS_URL loaded but invalid.")
        except ValueError:
            logger.error("SUCCESS_URL loaded but invalid.")
    else:
        logger.error("Failed to load SUCCESS_URL.")

    # quart
    jwt_secret_key = os.environ.get('JWT_SECRET_KEY')
    if jwt_secret_key:
        logger.info("JWT_SECRET_KEY loaded successfully.")
    else:
        logger.error("Failed to load JWT_SECRET_KEY.")
except Exception as e:
    logger.error("Missing one or more crucial environmental variables.")
    raise Exception("Missing one or more crucial environmental variables.") from None

# setup
logger.info('Starting the application...')
app = Quart(__name__)
rate_limiter = RateLimiter(app)
app.register_blueprint(dashboard_bp)
app.register_blueprint(signup_bp)

cors(app)  # this will enable CORS for all routes

app.user_database = UnionDatabase()

app.config['JWT_SECRET_KEY'] = jwt_secret_key
jwt = JWTManager(app)

# instantiate database
user_database = app.user_database

# rate limiter (redis)
redis_store = RedisStore(
    address="redis://localhost:6379/0",  # Replace with your Redis URL
    rate_limiter = RateLimiter(app)
)

# general routes
@app.route('/')
async def home():
    return redirect(url_for('signup.show_form'))

# life-cycle routes
@app.before_serving
async def startup():
    await user_database.create_pool()
    logger.info('Application has started.')

@app.after_serving
async def shutdown():
    await user_database.close_pool()
    logger.info('Application has stopped.')

if __name__ == '__main__':
    app.run()
