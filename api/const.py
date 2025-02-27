from load_dotenv import load_dotenv

from os import getenv

from router import router

load_dotenv(dotenv_path='.env')

DOCS_URL = getenv('API_DOCS_URL')
HOST = getenv('API_HOST')
PORT = int(getenv('API_PORT'))
BASE_PREFIX = getenv('API_PREFIX') if getenv('API_PREFIX') else ''

TITLE = 'API for signal 1win traffic-referral web app'
DESCRIPTION = ':3'

app_config = {
    "app_name": '1WIN SIGNAL API',
    "router": router,
    "docs_url": DOCS_URL,
    "host": HOST,
    "port": PORT,
    "base_prefix": BASE_PREFIX,
    "title": TITLE,
    "description": DESCRIPTION
}
