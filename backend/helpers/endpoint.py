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
