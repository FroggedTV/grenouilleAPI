import logging

from flask import request, jsonify

from helpers import UrlImageToBase64
from models import User

def build_api_user(app):
    """Factory to setup the routes for the user api."""

    @app.route('/api/user/details', methods=['GET'])
    def get_details():
        """
        @api {get} /api/user/details GetUserDetails
        @apiName GetUserDetails
        @apiGroup User
        @apiDescription This method returns multiple information about a user that logged at least one time.

        @apiParam {String} id SteamID (64bits) of the user to request.

        @apiSuccess {String} id SteamID (64bits).
        @apiSuccess {String} nickname Username.
        @apiSuccess {Boolean} nickname_verified True if user nickname is locked because verified.
        @apiSuccess {String} avatar User avatar as a 64bits string.

        @apiError (Errors){String} MissingIdParameter Id is not present in the parameters.
        @apiError (Errors){String} InvalidIdParameter Invalid id value (not an int).
        @apiError (Errors){String} UserNotFound There is no user in the database with this id.
        """
        steam_id = request.args.get('id', None)
        if steam_id is None:
            return jsonify({'success': 'no',
                            'error': 'MissingIdParameter',
                            'payload': {}
                            }), 200
        try:
            steam_id = int(steam_id)
        except ValueError:
            return jsonify({'success': 'no',
                            'error': 'InvalidIdParameter',
                            'payload': {}
                            }), 200
        user = User.get(steam_id)
        if user is None:
            return jsonify({'success': 'no',
                            'error': 'UserNotFound',
                            'payload': {}
                            }), 200

        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {
                        'id': str(user.id),
                        'nickname': user.nickname,
                        'nickname_verified': user.nickname_verified,
                        'avatar': user.avatar,

                    }}), 200
