from os.path import isfile
import os
import logging

class Config(object):
    """Basic configuration used by the application.

    Attributes:
        DEBUG: Flask debugging option.
        TESTING: Flask testing option.
        SQLALCHEMY_TRACK_MODIFICATIONS: Flask SQLalchmey track modifications 
        option.
        DATABASE_URI: Url to the database used in Flask.
    """
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/sqlite.db'.format(os.path.join(os.path.dirname(__file__)))
    HOST = '127.0.0.1'
    PORT = 9999
    SERVERNAME = 'http://127.0.0.1:9999'
    STEAM_KEY='XXX'
    FRONTEND_LOGIN_REDIRECT='http://127.0.0.1:9999/api/auth/token_test'
    API_KEY = 'abc'
    STEAM_BOTS = 'login1@pass1@login2@pass2'
    DOTA_LOBBY_CHEATS = False
    DOTA_LOBBY_TICKET = 0 # FTV 1 CUP is 4947 - FTV 2 LEAGUE is 9674

def load_config(config):
    """Load a configuration for the Flask application from a specific file.

    Starts with `Config` object as a base.
    Loads `settings.cfg` if exists and readable.

    Args:
        config: Application config object to load the config into.
    """
    config.from_object('cfg.configuration.Config')
    if isfile(os.path.join(os.path.dirname(__file__), 'settings.cfg')):
        try:
            config.from_pyfile(os.path.join(os.path.dirname(__file__), 'settings.cfg'))
        except SyntaxError:
            logging.log(logging.ERROR, 'Impossible to interpret settings file, using default.')
