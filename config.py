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
    YANDEX_APIKEY = os.environ['YANDEX_APIKEY']


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "real_secret"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.abspath(os.getcwd())+'\database.db'
    YANDEX_APIKEY = os.environ['YANDEX_APIKEY']


class TestingConfig(Config):
    TESTING = True