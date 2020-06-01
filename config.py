import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '3b4be1bd-c8a8-466d-bffd-9ac2a2de6c8c'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PG_CONNECTION = os.getenv("PG_CONNECTION")
    ORA_CONNECTION = os.getenv("ORA_CONNECTION")

    if PG_CONNECTION:
        SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_CONNECTION}'
    if ORA_CONNECTION:
        SQLALCHEMY_DATABASE_URI = f'oracle://{ORA_CONNECTION}'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True