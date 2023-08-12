import logging
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

ENVIRONMENT = os.environ.get('LOGGER_ENV')

LOG_LEVELS = {
    "development": logging.DEBUG,
    "staging": logging.INFO,
    "production": logging.WARNING
}

logging.basicConfig(
    filename=None,
    level=LOG_LEVELS.get(ENVIRONMENT, logging.WARNING),  # Default to WARNING if environment not recognized
    format='%(asctime)s %(levelname)s:%(message)s'
)

from payapp import app

app.run(
    debug=True if ENVIRONMENT == "development" else False,
    host="0.0.0.0",
    port=8000
)
