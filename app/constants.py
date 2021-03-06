import os

TMP_FOLDER = '/tmp/'
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
MONGO_DB_CONNECTION = os.environ.get('MONGO_DB_CONNECTION')
DANA_WEB_DATABASE = os.environ.get('DANA_WEB_DATABASE', "light")
CUSTOMER_TYPES = {'user': 'user', 'organization':'organization'}