from functools import wraps
import jwt
import logging

from flask import request, jsonify

def secure(app, type, scopes):
    """Decorator to turn a endpoint into a secure endpoint where a AuthToken is necessary, and scopes too.

    May raise AuthorizationHeaderInvalid, AuthTokenExpired, AuthTokenInvalid, ClientAccessImpossible,
    or ClientAccessRefused instead of calling the decorated function.
    Decorated function will be called with the auth token as a first argument.

    Args:
        app: Flask app to access config where the API_KEY is stored.
        type: List of type of Auth token accepted.
        scopes: list of scopes necessary to call the endpoint.
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
            if auth_token['client']['type'] not in type:
                return jsonify({'success': 'no',
                                'error': 'ClientAccessImpossible',
                                'payload': {}
                                }), 200
            for scope in scopes:
                if scope not in auth_token['client']['scopes']:
                    return jsonify({'success': 'no',
                                    'error': 'ClientAccessRefused',
                                    'payload': {}
                                    }), 200

            return f(auth_token, *args, **kwargs)

        return wrap

    return secured
