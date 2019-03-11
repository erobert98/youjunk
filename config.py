import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgres://dveqlsgrtftfdx:52e239ef3405006574af50d047e5471d92701851c178324be5e3dc6e9a0ed30e@ec2-54-235-133-42.compute-1.amazonaws.com:5432/d7h7vcorntejtl'
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


