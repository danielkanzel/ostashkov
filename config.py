import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET']
    SQLALCHEMY_DATABASE_URI = os.environ['HEROKU_POSTGRESQL_JADE_URL'] 



class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "real_secret"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.abspath(os.getcwd())+'\database.db'
    YANDEX_APIKEY = "3bda5c34-41cd-4840-8bc5-6dfe13e3aad4"


class TestingConfig(Config):
    TESTING = True