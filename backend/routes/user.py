import logging

from flask import request, jsonify
from models import User

def build_api_user(app):
    """Factory to setup the routes for the user api."""

    @app.route('/api/user/details', methods=['GET'])
    def get_user_details():
        """
        @api {get} /api/user/details UserGetDetails
        @apiVersion 1.0.4
        @apiName UserGetDetails
        @apiGroup User
        @apiDescription This method returns multiple information about a user that logged at least one time.

        @apiParam {String} id SteamID (64bits) of the user to request.
        @apiError (Errors){String} MissingIdParameter Id is not present in the parameters.
        @apiError (Errors){String} InvalidIdParameter Invalid id value (not an int).
        @apiError (Errors){String} UserNotFound There is no user in the database with this id.

        @apiSuccess {String} id SteamID (64bits).
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
                        'id': str(user.id)
                    }}), 200
