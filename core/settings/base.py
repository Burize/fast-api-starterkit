import os

IS_TEST = os.getenv('ENVIRONMENT') == 'test'
API_PREFIX = '/api'
DATABASE_URL = os.getenv('DATABASE_URL') if not IS_TEST else None
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
