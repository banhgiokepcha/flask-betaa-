import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object): 
   GOOGLE_MAPS_KEY = 'AIzaSyCJqpC7oo-YYJJ1pRVZJgf84qExlHZCWSc'
   GOOGLE_CLIENT_ID = "99789002244-ebk83arliq3r6l9hai7pb2m2s8l8bah7.apps.googleusercontent.com"
   GOOGLE_CLIENT_SECRET = "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"
  # GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
   SERVER_NAME = '127.0.0.1:5000'
   APPLICATION_ROOT = '/'
   PREFERRED_URL_SCHEME = 'http'
   
class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'webappmap.db')


class DevConfig(Config):
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'webappmap.db')