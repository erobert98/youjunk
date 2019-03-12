import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgres://rqvkuhlratqbny:82825d01568d3afbe704e2735d20f993e12fd8c0037f4780d0059678528e4b28@ec2-54-228-252-67.eu-west-1.compute.amazonaws.com:5432/dbqbkmp55dpu7g'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_URI = 'https://www.googleapis.com/oauth2/v3/token'

# class Auth:
#     CLIENT_ID = (
#         '265572427706-npsfsmdla38v2801c6t702aj5d0mn59u  \
#         .apps.googleusercontent.com')
#     CLIENT_SECRET = 'AaD_UikjVCia9yH7tbicmj5T'
#     REDIRECT_URI = 'http://localhost'
#     AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
#     TOKEN_URI = 'https://www.googleapis.com/oauth2/v3/token'
#     USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
#     SCOPE = 'https://www.googleapis.com/auth/youtube.readonly, https://www.googleapis.com/auth/youtube, https://www.googleapis.com/auth/youtube.upload'



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




config = {
    "dev": DevelopmentConfig,
    "prod": Config,
    "default": DevelopmentConfig
}


