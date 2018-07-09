from functools import wraps

from flask import request, jsonify

def api_key_endpoint(app):
    """Decorator to turn a endpoint into a secure endpoint where a API_KEY is necessary.

    Args:
        app: Flask app to access config where the API_KEY is stored.
    Returns:
        Decorated function.
    """
    def api_key_routed(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            header_key = request.headers.get('API_KEY', None)
            if header_key is None:
                return jsonify({'success': 'no',
                                'error': 'ApiKeyMissing',
                                'payload': {}
                                }), 200
            if header_key != app.config['API_KEY']:
                return jsonify({'success': 'no',
                                'error': 'ApiKeyInvalid',
                                'payload': {}
                                }), 200

            return f(*args, **kwargs)

        return wrap

    return api_key_routed

def user_endpoint(app, necessary_rights=None):
    """Decorator to turn a endpoint into a secure endpoint where a user Authorization is necessary.

    Args:
        app: Flask app to access config where the API_KEY is stored.
        necessary_rights: List of necessary user rights to use the endpoint. None is no right.
    Returns:
        Decorated function.
    """
    def user_routed(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            header_token = request.headers.get('Authorization', None)
            if (header_token is None
                    or len(header_token) < 8
                    or header_token[0:7] != 'Bearer '):
                return jsonify({'success': 'no',
                                'error': 'InvalidAuthorizationHeader',
                                'payload': {}
                                }), 200
            raw_token = header_token[7:]
            try:
                token = jwt.decode(raw_token,
                                   app.config['SECRET_KEY'],
                                   audience='refresh')
                if not(necessary_rights is None or 'all' in token['rights']):
                    # TODO test rights against arguments
                    pass

            except Exception as e:
                return jsonify({'success': 'no',
                                'error': 'InvalidRefreshToken',
                                'payload': {}
                                }), 200
            return f(*args, **kwargs)

        return wrap

    return user_routed

def user_or_api_key_endpoint(app):
    """Decorator to turn a endpoint into a secure endpoint where a API_KEY or a user Authorization is necessary.

    Args:
        app: Flask app to access config where the API_KEY is stored.
    Returns:
        Decorated function.
    """
    def user_or_api_key_routed(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            header_key = request.headers.get('API_KEY', None)
            if header_key is None:
                return jsonify({'success': 'no',
                                'error': 'ApiKeyMissing',
                                'payload': {}
                                }), 200
            if header_key != app.config['API_KEY']:
                return jsonify({'success': 'no',
                                'error': 'ApiKeyInvalid',
                                'payload': {}
                                }), 200

            return f(*args, **kwargs)

        return wrap

    return user_or_api_key_routed
