import logging
import re
import jwt
import hashlib

from datetime import datetime, timedelta
from steam import SteamID

from flask import jsonify, redirect, request
from helpers.endpoint import secure
from models import db, User, APIKey, UserScope, APIKeyScope, Scope

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
        user.refresh_token = token.decode('utf-8')
        db.session.commit()

        url = '{0}?token={1}'.format(app.config['FRONTEND_LOGIN_REDIRECT'],
                                     user.refresh_token)
        return redirect(url)

    @app.route('/api/auth/login/key', methods=['GET'])
    def login_key():
        """
        @api {get} /api/auth/login/key RefreshTokenGetWithKey
        @apiVersion 1.1.0
        @apiName RefreshTokenGetWithKey
        @apiGroup Authentication
        @apiDescription Get a refresh token using a API Key.

        @apiHeader {String} API_KEY API_KEY necessary to call the endpoint.
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
        if len(header_key)==0:
            return jsonify({'success': 'no',
                            'error': 'ApiKeyInvalid',
                            'payload': {}
                            }), 200

        salt = app.config['API_KEY_SALT']
        hash_object = hashlib.sha1((header_key + salt).encode('utf-8'))
        hash_key = hash_object.hexdigest()
        key = APIKey.get(hash_key)

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
            key.refresh_token = token.decode('utf-8')
            db.session.commit()
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {'token': key.refresh_token}
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

        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization header not well formated.
        @apiError (Errors){String} RefreshTokenExpired Refresh token has expired and client should get a new one.
        @apiError (Errors){String} RefreshTokenRevoked Refresh token has has been revoked and client should get a new one.
        @apiError (Errors){String} RefreshTokenInvalid Token is invalid (decode, rights, signature...).
        """
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
            refresh_token = jwt.decode(raw_token,
                               app.config['SECRET_KEY'],
                               audience='refresh')
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
                'type': refresh_token['client']['type']
            },
            'exp': datetime.utcnow() + timedelta(hours=1)
        }

        if refresh_token['client']['type'] == 'user':
            auth_token['client']['steamid'] = refresh_token['client']['steamid']
            # Test revoke
            user = User.get(refresh_token['client']['steamid'])
            if user is None or user.refresh_token != raw_token:
                return jsonify({'success': 'no',
                                'error': 'RefreshTokenRevoked',
                                'payload': {}
                                }), 200
            # Add scopes
            auth_token['client']['scopes'] = UserScope.get_all(refresh_token['client']['steamid'])
        elif refresh_token['client']['type'] == 'key':
            auth_token['client']['keyid'] = refresh_token['client']['keyid']
            # Test revoke
            key = APIKey.get(refresh_token['client']['keyid'])
            if key is None or key.refresh_token != raw_token:
                return jsonify({'success': 'no',
                                'error': 'RefreshTokenRevoked',
                                'payload': {}
                                }), 200
            # Add scopes
            auth_token['client']['scopes'] = APIKeyScope.get_all(refresh_token['client']['keyid'])

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

    @app.route('/api/auth/scope/list', methods=['GET'])
    @secure(app, ['key', 'user'], [])
    def get_scope_list(auth_token):
        """
        @api {get} /api/auth/scope/list ScopeList
        @apiVersion 1.1.0
        @apiName ScopeList
        @apiGroup Authentication
        @apiDescription List all available scopes for APIKey and users.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.

        @apiSuccess {String[]} scopes All available scopes.
        """
        scopes = []
        for scope in list(Scope):
            scopes.append(scope.value)
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {'scopes': scopes}
                        }), 200

    @app.route('/api/auth/key/list', methods=['GET'])
    @secure(app, ['key', 'user'], ['api_key_scope'])
    def get_api_key_list(auth_token):
        """
        @api {get} /api/auth/key/list APIKeyList
        @apiVersion 1.1.0
        @apiName APIKeyList
        @apiGroup Authentication
        @apiDescription List all APIKeys.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {Integer{1-100}} [limit=10] Optional number of entries to return.
        @apiError (Errors){String} LimitInvalid Limit is not a positive integer in waited range.
        @apiParam {Integer{0-..}} [offset=0] Optional offset for database fetch.
        @apiError (Errors){String} OffsetInvalid Offset is not a positive integer in waited range.

        @apiSuccess {Object[]} keys All available scopes.
        @apiSuccess {String} keys.hash Hash of the API_KEY.
        @apiSuccess {String} keys.description API Key description.
        @apiSuccess {String[]} keys.scopes List of scopes this KEY has access to.
        """
        data = request.get_json(force=True)

        # limit check
        limit = data.get('limit', 10)
        if not isinstance(limit, int) or limit <= 0 or limit > 100:
            return jsonify({'success': 'no',
                            'error': 'LimitInvalid',
                            'payload': {}
                            }), 200

        # offset check
        offset = data.get('offset', 0)
        if not isinstance(offset, int) or offset < 0 :
            return jsonify({'success': 'no',
                            'error': 'OffsetInvalid',
                            'payload': {}
                            }), 200

        # Return results
        keys = []
        for api_key in db.session().query(APIKey)\
                                   .order_by(APIKey.key_hash.desc())\
                                   .limit(limit)\
                                   .offset(offset)\
                                   .all():
            scopes = []
            for scope in db.session().query(APIKeyScope).filter(APIKeyScope.key_hash==api_key.key_hash).all():
                scopes.append(scope.scope)
            keys.append({ 'hash': api_key.key_hash, 'description': api_key.description, 'scopes': scopes })
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {
                            'keys': keys
                        }
                        }), 200

    @app.route('/api/auth/key/add', methods=['POST'])
    @secure(app, ['key', 'user'], ['api_key_scope'])
    def post_api_key_add(auth_token):
        """
        @api {post} /api/auth/key/add APIKeyAdd
        @apiVersion 1.1.0
        @apiName APIKeyAdd
        @apiGroup Authentication
        @apiDescription Add a new APIKey into the system.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} key APIKey to add to the system.
        @apiError (Errors){String} KeyParameterMissing Key is not present in the parameters.
        @apiError (Errors){String} KeyParameterInvalid Key is not valid String.
        @apiError (Errors){String} KeyAlreadyExists Key is already in the system.
        @apiParam {String} description Key description for information.
        @apiError (Errors){String} DescriptionParameterMissing Description is not present in the parameters.
        @apiError (Errors){String} DescriptionParameterInvalid Description is not valid String.
        """
        data = request.get_json(force=True)

        # key checks
        key = data.get('key', None)
        if key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(key, str) or len(key) == 0:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterInvalid',
                            'payload': {}
                            }), 200

        # description checks
        description = data.get('description', None)
        if description is None:
            return jsonify({'success': 'no',
                            'error': 'DescriptionParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(description, str) or len(description) == 0:
            return jsonify({'success': 'no',
                            'error': 'DescriptionParameterInvalid',
                            'payload': {}
                            }), 200

        # Hash
        salt = app.config['API_KEY_SALT']
        hash_object = hashlib.sha1((key + salt).encode('utf-8'))
        hash_key = hash_object.hexdigest()
        db_key = APIKey.get(hash_key)

        if db_key is not None:
            return jsonify({'success': 'no',
                            'error': 'KeyAlreadyExists',
                            'payload': {}
                            }), 200
        db_key = APIKey(hash_key, description)
        db.session().add(db_key)
        db.session().commit()
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200

    @app.route('/api/auth/key/remove', methods=['POST'])
    @secure(app, ['key', 'user'], ['api_key_scope'])
    def post_api_key_remove(auth_token):
        """
        @api {post} /api/auth/key/remove APIKeyRemove
        @apiVersion 1.1.0
        @apiName APIKeyRemove
        @apiGroup Authentication
        @apiDescription Remove an APIKey from the system.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} key APIKey to add to the system.
        @apiError (Errors){String} KeyParameterMissing Key is not present in the parameters.
        @apiError (Errors){String} KeyParameterInvalid Key is not valid String.
        @apiError (Errors){String} KeyDoesntExists There is no such key in the system.
        """
        data = request.get_json(force=True)

        # key checks
        key = data.get('key', None)
        if key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(key, str) or len(key) == 0:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterInvalid',
                            'payload': {}
                            }), 200

        # Hash
        salt = app.config['API_KEY_SALT']
        hash_object = hashlib.sha1((key + salt).encode('utf-8'))
        hash_key = hash_object.hexdigest()
        db_key = APIKey.get(hash_key)

        if db_key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyDoesntExists',
                            'payload': {}
                            }), 200
        db.session().delete(db_key)
        db.session().commit()
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200

    @app.route('/api/auth/key/description/update', methods=['POST'])
    @secure(app, ['key', 'user'], ['api_key_scope'])
    def post_api_key_description_update(auth_token):
        """
        @api {post} /api/auth/key/description/update APIKeyDescriptionUpdate
        @apiVersion 1.1.0
        @apiName APIKeyDescriptionUpdate
        @apiGroup Authentication
        @apiDescription Update the description of an APIKey.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} key APIKey to update the description.
        @apiError (Errors){String} KeyParameterMissing Key is not present in the parameters.
        @apiError (Errors){String} KeyParameterInvalid Key is not valid String.
        @apiError (Errors){String} KeyDoesntExists There is no such key in the system.
        @apiParam {String} description Key description for information.
        @apiError (Errors){String} DescriptionParameterMissing Description is not present in the parameters.
        @apiError (Errors){String} DescriptionParameterInvalid Description is not valid String.
        """
        data = request.get_json(force=True)

        # key checks
        key = data.get('key', None)
        if key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(key, str) or len(key) == 0:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterInvalid',
                            'payload': {}
                            }), 200

        # description checks
        description = data.get('description', None)
        if description is None:
            return jsonify({'success': 'no',
                            'error': 'DescriptionParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(description, str) or len(description) == 0:
            return jsonify({'success': 'no',
                            'error': 'DescriptionParameterInvalid',
                            'payload': {}
                            }), 200

        # Hash
        salt = app.config['API_KEY_SALT']
        hash_object = hashlib.sha1((key + salt).encode('utf-8'))
        hash_key = hash_object.hexdigest()
        db_key = APIKey.get(hash_key)

        if db_key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyDoesntExists',
                            'payload': {}
                            }), 200
        db_key.description = description
        db.session().commit()
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200

    @app.route('/api/auth/key/scope/add', methods=['POST'])
    @secure(app, ['key', 'user'], ['api_key_scope'])
    def post_api_key_scope_add(auth_token):
        """
        @api {post} /api/auth/key/scope/add APIKeyScopeAdd
        @apiVersion 1.1.0
        @apiName APIKeyScopeAdd
        @apiGroup Authentication
        @apiDescription Add scope access to the APIKey.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} key APIKey to add scopes to.
        @apiError (Errors){String} KeyParameterMissing Key is not present in the parameters.
        @apiError (Errors){String} KeyParameterInvalid Key is not valid String.
        @apiError (Errors){String} KeyDoesntExists There is no such key in the system.
        @apiParam {String[]} scopes Scopes to add to the key.
        @apiError (Errors){String} ScopesParameterMissing Scope is not present in the parameters.
        @apiError (Errors){String} ScopesParameterInvalid Scope is not list of valid scope Strings.
        """
        data = request.get_json(force=True)

        # key checks
        key = data.get('key', None)
        if key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(key, str) or len(key) == 0:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterInvalid',
                            'payload': {}
                            }), 200

        # scopes checks
        scopes = data.get('scopes', None)
        if scopes is None:
            return jsonify({'success': 'no',
                            'error': 'ScopesParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(scopes, list) or len(scopes) == 0:
            return jsonify({'success': 'no',
                            'error': 'ScopesParameterInvalid',
                            'payload': {}
                            }), 200
        all_scopes = [x.value for x in list(Scope)]
        for scope in scopes:
            if scope not in all_scopes:
                return jsonify({'success': 'no',
                                'error': 'ScopesParameterInvalid',
                                'payload': {}
                                }), 200
        # Hash
        salt = app.config['API_KEY_SALT']
        hash_object = hashlib.sha1((key + salt).encode('utf-8'))
        hash_key = hash_object.hexdigest()
        db_key = APIKey.get(hash_key)

        if db_key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyDoesntExists',
                            'payload': {}
                            }), 200

        # add scopes
        for scope in scopes:
            APIKeyScope.upsert(hash_key, scope)
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200

    @app.route('/api/auth/key/scope/remove', methods=['POST'])
    @secure(app, ['key', 'user'], ['api_key_scope'])
    def post_api_key_scope_remove(auth_token):
        """
        @api {post} /api/auth/key/scope/remove APIKeyScopeRemove
        @apiVersion 1.1.0
        @apiName APIKeyScopeRemove
        @apiGroup Authentication
        @apiDescription Remove scope access to the APIKey.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} key APIKey to remove scopes from.
        @apiError (Errors){String} KeyParameterMissing Key is not present in the parameters.
        @apiError (Errors){String} KeyParameterInvalid Key is not valid String.
        @apiError (Errors){String} KeyDoesntExists There is no such key in the system.
        @apiParam {String[]} scopes Scopes to remove from the key.
        @apiError (Errors){String} ScopesParameterMissing Scope is not present in the parameters.
        @apiError (Errors){String} ScopesParameterInvalid Scope is not list of valid scope Strings.
        """
        data = request.get_json(force=True)

        # key checks
        key = data.get('key', None)
        if key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(key, str) or len(key) == 0:
            return jsonify({'success': 'no',
                            'error': 'KeyParameterInvalid',
                            'payload': {}
                            }), 200

        # scopes checks
        scopes = data.get('scopes', None)
        if scopes is None:
            return jsonify({'success': 'no',
                            'error': 'ScopesParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(scopes, list) or len(scopes) == 0:
            return jsonify({'success': 'no',
                            'error': 'ScopesParameterInvalid',
                            'payload': {}
                            }), 200
        all_scopes = [x.value for x in list(Scope)]
        for scope in scopes:
            if scope not in all_scopes:
                return jsonify({'success': 'no',
                                'error': 'ScopesParameterInvalid',
                                'payload': {}
                                }), 200
        # Hash
        salt = app.config['API_KEY_SALT']
        hash_object = hashlib.sha1((key + salt).encode('utf-8'))
        hash_key = hash_object.hexdigest()
        db_key = APIKey.get(hash_key)

        if db_key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyDoesntExists',
                            'payload': {}
                            }), 200

        # remove scopes
        for scope in scopes:
            api_scope = db.session.query(APIKeyScope).filter(APIKeyScope.key_hash==hash_key, APIKeyScope.scope==scope).one_or_none()
            if api_scope is not None:
                db.session.delete(api_scope)
        db.session.commit()
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200

    @app.route('/api/auth/user/scope/list', methods=['GET'])
    @secure(app, ['key', 'user'], ['user_scope'])
    def get_user_scope_list(auth_token):
        """
        @api {get} /api/auth/user/scope/list UserScopeList
        @apiVersion 1.1.0
        @apiName UserScopeList
        @apiGroup Authentication
        @apiDescription List all users with their scopes.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {Integer{1-100}} [limit=10] Optional number of entries to return.
        @apiError (Errors){String} LimitInvalid Limit is not a positive integer in waited range.
        @apiParam {Integer{0-..}} [offset=0] Optional offset for database fetch.
        @apiError (Errors){String} OffsetInvalid Offset is not a positive integer in waited range.

        @apiSuccess {Number} total Total number of users.
        @apiSuccess {Object[]} users All available users.
        @apiSuccess {String} users.id Id of the user.
        @apiSuccess {String[]} users.scopes List of scopes this user has access to.
        """
        data = request.get_json(force=True)

        # limit check
        limit = data.get('limit', 10)
        if not isinstance(limit, int) or limit <= 0 or limit > 100:
            return jsonify({'success': 'no',
                            'error': 'LimitInvalid',
                            'payload': {}
                            }), 200

        # offset check
        offset = data.get('offset', 0)
        if not isinstance(offset, int) or offset < 0 :
            return jsonify({'success': 'no',
                            'error': 'OffsetInvalid',
                            'payload': {}
                            }), 200

        # Return results
        total = db.session().query(User).count()
        users = []
        for user in db.session().query(User)\
                                   .order_by(User.id.desc())\
                                   .limit(limit)\
                                   .offset(offset)\
                                   .all():
            scopes = []
            for scope in db.session().query(UserScope).filter(UserScope.id==user.id).all():
                scopes.append(scope.scope)
            users.append({ 'id': user.id, 'scopes': scopes })
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {
                            'total': total,
                            'users': users
                        }
                        }), 200

    @app.route('/api/auth/user/scope/add', methods=['POST'])
    @secure(app, ['key', 'user'], ['user_scope'])
    def post_user_scope_add(auth_token):
        """
        @api {post} /api/auth/user/scope/add UserScopeAdd
        @apiVersion 1.1.0
        @apiName UserScopeAdd
        @apiGroup Authentication
        @apiDescription Add scope access to a user.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} id User id to add scopes to.
        @apiError (Errors){String} IdParameterMissing id is not present in the parameters.
        @apiError (Errors){String} IdParameterInvalid id is not valid String.
        @apiError (Errors){String} UserWithIdDoesntExists There is no user with such id in the system.
        @apiParam {String[]} scopes Scopes to add to the user.
        @apiError (Errors){String} ScopesParameterMissing Scope is not present in the parameters.
        @apiError (Errors){String} ScopesParameterInvalid Scope is not list of valid scope Strings.
        """
        data = request.get_json(force=True)

        # key checks
        id = data.get('id', None)
        if id is None:
            return jsonify({'success': 'no',
                            'error': 'IdParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(id, int) or id <=0:
            return jsonify({'success': 'no',
                            'error': 'IdParameterInvalid',
                            'payload': {}
                            }), 200

        # scopes checks
        scopes = data.get('scopes', None)
        if scopes is None:
            return jsonify({'success': 'no',
                            'error': 'ScopesParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(scopes, list) or len(scopes) == 0:
            return jsonify({'success': 'no',
                            'error': 'ScopesParameterInvalid',
                            'payload': {}
                            }), 200
        all_scopes = [x.value for x in list(Scope)]
        for scope in scopes:
            if scope not in all_scopes:
                return jsonify({'success': 'no',
                                'error': 'ScopesParameterInvalid',
                                'payload': {}
                                }), 200

        # Hash
        user = User.get(id)

        if user is None:
            return jsonify({'success': 'no',
                            'error': 'UserWithIdDoesntExists',
                            'payload': {}
                            }), 200

        # add scopes
        for scope in scopes:
            UserScope.upsert(id, scope)
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200

    @app.route('/api/auth/user/scope/remove', methods=['POST'])
    @secure(app, ['key', 'user'], ['user_scope'])
    def post_user_scope_remove(auth_token):
        """
        @api {post} /api/auth/user/scope/remove UserScopeRemove
        @apiVersion 1.1.0
        @apiName UserScopeRemove
        @apiGroup Authentication
        @apiDescription Remove scope access from a user.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} id User id to remove scopes from.
        @apiError (Errors){String} IdParameterMissing id is not present in the parameters.
        @apiError (Errors){String} IdParameterInvalid id is not valid String.
        @apiError (Errors){String} UserWithIdDoesntExists There is no user with such id in the system.
        @apiParam {String[]} scopes Scopes to remove from the user.
        @apiError (Errors){String} ScopesParameterMissing Scope is not present in the parameters.
        @apiError (Errors){String} ScopesParameterInvalid Scope is not list of valid scope Strings.
        """
        data = request.get_json(force=True)

        # key checks
        id = data.get('id', None)
        if id is None:
            return jsonify({'success': 'no',
                            'error': 'IdParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(id, int) or id <=0:
            return jsonify({'success': 'no',
                            'error': 'IdParameterInvalid',
                            'payload': {}
                            }), 200

        # scopes checks
        scopes = data.get('scopes', None)
        if scopes is None:
            return jsonify({'success': 'no',
                            'error': 'ScopesParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(scopes, list) or len(scopes) == 0:
            return jsonify({'success': 'no',
                            'error': 'ScopesParameterInvalid',
                            'payload': {}
                            }), 200
        all_scopes = [x.value for x in list(Scope)]
        for scope in scopes:
            if scope not in all_scopes:
                return jsonify({'success': 'no',
                                'error': 'ScopesParameterInvalid',
                                'payload': {}
                                }), 200

        # Hash
        user = User.get(id)
        if user is None:
            return jsonify({'success': 'no',
                            'error': 'UserWithIdDoesntExists',
                            'payload': {}
                            }), 200

        # add scopes
        for scope in scopes:
            user_scope = db.session.query(UserScope).filter(UserScope.id==user.id, UserScope.scope==scope).one_or_none()
            if user_scope is not None:
                db.session.delete(user_scope)
        db.session.commit()
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200
