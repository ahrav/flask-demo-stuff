import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get["PROD_DATABASE_URL"]
