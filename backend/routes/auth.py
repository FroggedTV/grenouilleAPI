import logging
import re
import jwt
import hashlib

from datetime import datetime, timedelta
from steam import SteamID

from flask import jsonify, redirect, request
from models import db, UserRefreshToken, User, APIKey

def build_api_auth(app, oid):
    """Factory to setup the routes for the auth api."""

    @app.route('/api/auth/login/steam', methods=['GET'])
    @oid.loginhandler
    def login_steam():
        """
        @api {get} /api/auth/login/steam RefreshTokenGetSteam
        @apiVersion 1.1.0
        @apiName RefreshTokenGetWithSteam
        @apiGroup Authentication
        @apiDescription First endpoint to call in the auth process with user. Calling it redirects to the steam login page.
        After login, the user is redirected to a callback url with the refresh token as a parameter.
        The URL is defined in the backend config. Frontend must be able to manage the token incoming as a parameter.
        """
        return oid.try_login('http://steamcommunity.com/openid')

    # Regex to get steam id from openid url
    _steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

    @oid.after_login
    def login_callback(resp):
        """Callback fired after steam login, log user in the application by generating a refresh token.
        Also create a basic user entry from steam id if this is the first login.

        Args:
            resp: OpenID response.
        Returns:
            Redirects to the callback url defined in the config with the refresh token as a parameter.
        """
        match = _steam_id_re.search(resp.identity_url)
        steam_id = SteamID(match.group(1))

        token = {
            'aud': 'refresh',
            'client': {
                'type': 'user',
                'steamid': str(steam_id.as_64)
            },
            'exp': datetime.utcnow() + timedelta(days=60)
        }
        token = jwt.encode(token, app.config['SECRET_KEY'])

        user = User.get(steam_id)
        if user is None:
            user = User(steam_id)
            db.session.add(user)
        UserRefreshToken.upsert(steam_id, token.decode('utf-8'))
        db.session.commit()

        url = '{0}?token={1}'.format(app.config['FRONTEND_LOGIN_REDIRECT'],
                                     token.decode('utf-8'))
        return redirect(url)

    @app.route('/api/auth/login/key', methods=['GET'])
    def login_key():
        """
        @api {get} /api/auth/login/key RefreshTokenGetWithKey
        @apiVersion 1.1.0
        @apiName RefreshTokenGetWithKey
        @apiGroup Authentication
        @apiDescription Get a refresh token using a API Key.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiSuccess {String} token Refresh token long lived to request access data.
        """
        header_key = request.headers.get('API_KEY', None)
        if header_key is None:
            return jsonify({'success': 'no',
                            'error': 'ApiKeyMissing',
                            'payload': {}
                            }), 200

        salt = app.config['API_KEY_SALT']
        hash_object = hashlib.sha1(header_key + salt)
        hash_key = hash_object.hexdigest()
        key = APIKey.get(hash_key.decode('utf-8'))

        if key is None:
            return jsonify({'success': 'no',
                            'error': 'ApiKeyInvalid',
                            'payload': {}
                            }), 200
        else:
            token = {
                'aud': 'refresh',
                'client': {
                    'type': 'key',
                    'keyid': str(key.key_hash)
                },
                'exp': datetime.utcnow() + timedelta(days=60)
            }
            token = jwt.encode(token, app.config['SECRET_KEY'])
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {'token': token.decode('utf-8')}
                            }), 200

    @app.route('/api/auth/token', methods=['GET'])
    def get_auth_token():
        """
        @api {get} /api/auth/token AuthTokenGet
        @apiVersion 1.1.0
        @apiName AuthTokenGet
        @apiGroup Authentication
        @apiDescription Refresh tokens are long lived but auth tokens are short lived.
        Using a valid refresh token, this api delivers an auth token to access data endpoints.

        @apiHeader {String} Authorization 'Bearer <refresh_token>'

        @apiSuccess {String} token Authentication token short lived to access data.

        @apiError (Errors){String} HeaderInvalid Authorization header not well formated.
        @apiError (Errors){String} RefreshTokenMissing There is no refresh token provided.
        @apiError (Errors){String} RefreshTokenExpired Refresh token has expired and client should get a new one.
        @apiError (Errors){String} RefreshTokenInvalid Token is invalid (decode, rights, signature...).
        """
        header_token = request.headers.get('Authorization', None)
        if (header_token is None
            or len(header_token) < 8
            or header_token[0:7] != 'Bearer '):
            return jsonify({'success': 'no',
                            'error': 'HeaderInvalid',
                            'payload': {}
                            }), 200
        raw_token = header_token[7:]
        try:
            token = jwt.decode(raw_token,
                               app.config['SECRET_KEY'],
                               audience='refresh')
        except jwt.InvalidAudienceError:
            return jsonify({'success': 'no',
                            'error': 'RefreshTokenMissing',
                            'payload': {}
                            }), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'success': 'no',
                            'error': 'RefreshTokenExpired',
                            'payload': {}
                            }), 200
        except Exception as e:
            return jsonify({'success': 'no',
                            'error': 'RefreshTokenInvalid',
                            'payload': {}
                            }), 200

        auth_token = {
                'aud': 'auth',
                'client': {
                    'type': token['client']['type']
                },
                'exp': datetime.utcnow() + timedelta(hours=1)
            }

        if token['client']['type'] == 'user':
            auth_token['client']['steamid'] = token['client']['steamid']

            # Check if the refresh token is still valid
            # TODO
            # Add scopes
            # TODO
        elif token['client']['type'] == 'key':
            auth_token['client']['keyid'] = token['client']['keyid']

            # Check if the refresh token is still valid
            # TODO
            # Add scopes
            # TODO

        auth_token = jwt.encode(auth_token, app.config['SECRET_KEY'])
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {'token': auth_token.decode('utf-8')}
                        }), 200

    @app.route('/api/auth/token_test', methods=['GET'])
    def test_token_display():
        """ Dummy display of a Refresh Token. Test function used to display the token generated after the steam login.
        This must not be used in production, but only as a token displayer in dev.
        """
        token = request.args.get('token', '')
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {'token': token}
                        }), 200
