from functools import wraps
import jwt
import logging

from flask import request, jsonify

def secure(app):
    """Decorator to turn a endpoint into a secure endpoint where a AuthToken is necessary, and scopes too.

    May raise AuthorizationHeaderInvalid, AuthTokenExpired, AuthTokenInvalid, ClientAccessImpossible,
    or ClientAccessRefused instead of calling the decorated function.
    Decorated function will be called with the auth token as a first argument.

    Args:
        app: Flask app to access config where the API_KEY is stored.
    Returns:
        Decorated function.
    """
    def secured(f):
        @wraps(f)
        def wrap(*args, **kwargs):

            header_token = request.headers.get('Authorization', None)
            if (header_token is None
                    or len(header_token) < 8
                    or header_token[0:7] != 'Bearer '):
                return jsonify({'success': 'no',
                                'error': 'AuthorizationHeaderInvalid',
                                'payload': {}
                                }), 200
            raw_token = header_token[7:]
            try:
                auth_token = jwt.decode(raw_token,
                                        app.config['SECRET_KEY'],
                                        audience='auth')
            except jwt.ExpiredSignatureError:
                return jsonify({'success': 'no',
                                'error': 'AuthTokenExpired',
                                'payload': {}
                                }), 401
            except Exception as e:
                logging.error(e)
                return jsonify({'success': 'no',
                                'error': 'AuthTokenInvalid',
                                'payload': {}
                                }), 401

            return f(auth_token, *args, **kwargs)
        return wrap
    return secured

def is_client_authorized(auth_token, type):
    return auth_token['client']['type'] in type

def has_client_scope(auth_token, channel, scopes):
    for scope in scopes:
        if channel not in auth_token['client']['scopes']:
            return False
        if scope not in auth_token['client']['scopes'][channel]:
            return False
    return True
