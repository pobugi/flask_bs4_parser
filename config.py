import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = os.getenv("DATABASE_TEST_URL")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TEST_URL")
    USER = os.getenv("TEST_USER")
    USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
