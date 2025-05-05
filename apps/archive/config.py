import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT=os.environ.get('SECURITY_PASSWORD_SALT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    RUMBU_CEO = os.environ.get('RUMBU_CEO')
    RUMBU_HR_MANAGER = os.environ.get('RUMBU_HR_MANAGER')
    RUMBU_ACCOUNTANT = os.environ.get('RUMBU_ACCOUNTANT')
    RUMBU_SALES_DIRECTOR = os.environ.get('RUMBU_SALES_DIRECTOR')
    RUMBU_AGENTS_EMAILS = os.environ.get('RUMBU_AGENTS_EMAILS')
    BABEL_DEFAULT_LOCALE = 'fr'
    BABEL_SUPPORTED_LOCALES = ['en', 'fr', 'de', 'zh', 'ru', 'tr']
    BABEL_TRANSLATION_DIRECTORIES = './translations'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('ARCHIVE_DEV_DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('ARCHIVE_TEST_DATABASE_URL')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('ARCHIVE_PRODUCTION_DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
