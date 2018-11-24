import logging

from flask import request, jsonify
from steam import WebAPI

from database import db
from models.User import User
from helpers.general import safe_json_loads
from helpers.endpoint import secure, is_client_authorized, has_client_scope

def build_api_user(app):
    """Factory to setup the routes for the user api."""

    steam_api = WebAPI(app.config['STEAM_KEY'])

    @app.route('/api/user/me/details', methods=['GET'])
    @secure(app)
    def get_user_me_details(auth_token):
        """
        @api {get} /api/user/me/details UserMeDetails
        @apiVersion 1.2.0
        @apiName UserMeDetails
        @apiGroup User
        @apiDescription Get detailed information of myself, scopes, id...

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.

        @apiSuccess {Integer} steam_id Steam ID of the user.
        @apiSuccess {Dictionary} scopes Set of all scopes this user has access to.
        @apiSuccess {String} scopes.key Channel name.
        @apiSuccess {String[]} scopes.value List of scopes this user has access to on this channel.
        """
        if not is_client_authorized(auth_token, ['user']):
            return jsonify({'success': 'no', 'error': 'ClientAccessImpossible', 'payload': {}}), 403

        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {
                        'steam_id': str(auth_token['client']['steamid']),
                        'scopes': auth_token['client']['scopes']
                    }}), 200

    @app.route('/api/user/name/refresh', methods=['POST'])
    @secure(app)
    def post_user_name_refresh(auth_token):
        """
        @api {get} /api/user/name/refresh UserNameRefresh
        @apiVersion 1.2.0
        @apiName UserNameRefresh
        @apiGroup User
        @apiDescription Refresh the user name by fetching it from Steam services.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} id User id to refresh the name.
        @apiError (Errors){String} IdParameterMissing id is not present in the parameters.
        @apiError (Errors){String} IdParameterInvalid id is not valid String.
        @apiError (Errors){String} UserWithIdDoesntExists There is no user with such id in the system.
        @apiParam {String} channel Channel the user is used into (mainly to check caller rights).
        @apiError (Errors){String} ChannelParameterMissing Channel is not present in the parameters.
        @apiError (Errors){String} ChannelParameterInvalid Channel is not a valid String.
        @apiError (Errors){String} SteamFetchError Error during the steam fetch process.
        """
        data = request.get_json(force=True)

        # key checks
        id = data.get('id', None)
        if id is None:
            return jsonify({'success': 'no',
                            'error': 'IdParameterMissing',
                            'payload': {}
                            }), 200
        if not id.isdigit():
            return jsonify({'success': 'no',
                            'error': 'IdParameterInvalid',
                            'payload': {}
                            }), 200
        id = int(id)

        # channel check
        channel = data.get('channel', None)
        if channel is None:
            return jsonify({'success': 'no',
                            'error': 'ChannelParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(channel, str) or len(channel) == 0:
            return jsonify({'success': 'no',
                            'error': 'ChannelParameterInvalid',
                            'payload': {}
                            }), 200
        if not has_client_scope(auth_token, channel, ['user_scope']):
            return jsonify({'success': 'no', 'error': 'ClientAccessRefused', 'payload': {}}), 403

        user = User.get(id)

        if user is None:
            return jsonify({'success': 'no',
                            'error': 'UserWithIdDoesntExists',
                            'payload': {}
                            }), 200

        # FETCH NEW USER NAME TODO
        try:
            steam_fetch = steam_api.ISteamUser.GetPlayerSummaries(steamids=user.id)
            if ('response' in steam_fetch
                and 'players' in steam_fetch['response']
                and len(steam_fetch['response']['players'])>0
                and 'personaname' in steam_fetch['response']['players'][0]):
                user.name = steam_fetch['response']['players'][0]['personaname']
                db.session.commit()
        except Exception as e:
            return jsonify({'success': 'no',
                        'error': 'SteamFetchError',
                        'payload': {}}), 200

        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {
                        'id': str(user.id),
                        'name': user.name
                    }}), 200
