class Config(object):
    DEBUG = True
    SECRET_KEY = '32498jkhsf123fdh123j213l2131f2jewf1fe21f1y3'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db_notification.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigTest(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/db_test.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
