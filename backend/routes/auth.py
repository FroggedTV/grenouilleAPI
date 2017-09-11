import logging
import re
import jwt
from datetime import datetime, timedelta
from urllib.parse import urlencode

from flask import jsonify, redirect, request

from models import UserRefreshToken

def build_api_auth(app, oid):
    """Factory to setup the routes for the auth api."""

    @app.route('/api/auth/login', methods=['GET'])
    @oid.loginhandler
    def login():
        """Steam openid caller.

        Returns:
            Redirects to the steam login page.
        """
        return oid.try_login('http://steamcommunity.com/openid')

    # Regex to get steam id from openid url
    _steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

    @oid.after_login
    def login_callback(resp):
        """Callback fired after steam login, log user in the application.

        Args:
            resp: OpenID response.
        Returns:
            Generated refresh token.
        """
        match = _steam_id_re.search(resp.identity_url)
        steamid = int(match.group(1))

        token = {
            'steamid': str(steamid),
            'aud': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=60)
        }
        token = jwt.encode(token, app.config['SECRET_KEY'])

        UserRefreshToken.upsert(steamid, token.decode('utf-8'))

        url = '{0}?token={1}'.format(app.config['FRONTEND_LOGIN_REDIRECT'],
                                     token.decode('utf-8'))
        return redirect(url)


    @app.route('/api/auth/token_test', methods=['GET'])
    def test_token_display():
        """Test function used to display the token generated after the steam login.
        This will be replaced by the frontend listener.

        Args:
            The token to display."""
        token = request.args.get('token', '')
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {'token': token}
                        }), 200
