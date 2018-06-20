import logging
import re
import jwt
from datetime import datetime, timedelta
from steam import SteamID

from flask import jsonify, redirect, request

from models import db, UserRefreshToken, User

def build_api_auth(app, oid):
    """Factory to setup the routes for the auth api."""

    @app.route('/api/auth/login', methods=['GET'])
    @oid.loginhandler
    def login():
        """
        @api {get} /api/auth/login RefreshTokenGet
        @apiVersion 1.0.4
        @apiName RefreshTokenGet
        @apiGroup Authentication
        @apiDescription First endpoint to call in the auth process. Calling it redirects to the steam login page.
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
            'steamid': str(steam_id.as_64),
            'aud': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=60)
        }
        token = jwt.encode(token, app.config['SECRET_KEY'])

        UserRefreshToken.upsert(steam_id, token.decode('utf-8'))
        user = User.get(steam_id)
        if user is None:
            user = User(steam_id)
            db.session.add(user)
        db.session.commit()

        url = '{0}?token={1}'.format(app.config['FRONTEND_LOGIN_REDIRECT'],
                                     token.decode('utf-8'))
        return redirect(url)

    @app.route('/api/auth/token', methods=['GET'])
    def get_auth_token():
        """
        @api {get} /api/auth/token AuthTokenGet
        @apiVersion 1.0.4
        @apiName AuthTokenGet
        @apiGroup Authentication
        @apiDescription Refresh tokens are long lived but auth tokens are short lived.
        Using a valid refresh token, this api delivers an auth token to access data endpoints.

        @apiHeader {String} Authorization 'Bearer <refresh_token>'

        @apiSuccess {String} auth_token Authentication token short lived to access data.

        @apiError (Errors){String} InvalidHeader Authorization header not well formated.
        @apiError (Errors){String} NoRefreshToken There is no refresh token provided.
        @apiError (Errors){String} ExpiredRefreshToken Refresh token has expired and user should log again.
        @apiError (Errors){String} InvalidRefreshToken Token is invalid (decode, rights, signature...).
        """
        header_token = request.headers.get('Authorization', None)
        if (header_token is None
            or len(header_token) < 8
            or header_token[0:7] != 'Bearer '):
            return jsonify({'success': 'no',
                            'error': 'InvalidHeader',
                            'payload': {}
                            }), 200
        raw_token = header_token[7:]
        try:
            token = jwt.decode(raw_token,
                               app.config['SECRET_KEY'],
                               audience='refresh')
        except jwt.InvalidAudienceError:
            return jsonify({'success': 'no',
                            'error': 'NoRefreshToken',
                            'payload': {}
                            }), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'success': 'no',
                            'error': 'ExpiredRefreshToken',
                            'payload': {}
                            }), 200
        except Exception as e:
            return jsonify({'success': 'no',
                            'error': 'InvalidRefreshToken',
                            'payload': {}
                            }), 200

        steam_id = int(token['steamid'])

        # Check if this is the only valid refresh token
        user_refresh_token = UserRefreshToken.get(steam_id)
        if (user_refresh_token is None
            or user_refresh_token.refresh_token != raw_token):
            return jsonify({'success': 'no',
                            'error': 'ExpiredRefreshToken',
                            'payload': {}
                            }), 200

        auth_token = {
            'steamid': str(steam_id),
            'aud': 'auth',
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
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
