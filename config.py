import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    TEST = False
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/aion?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SECRET_KEY = str(os.urandom(48))[2:-1].replace('\\x', '')

    UNITPAY_SECRET_KEY = '00000000000000000000'