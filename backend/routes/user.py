import logging

from flask import request, jsonify
from models import User

def build_api_user(app):
    """Factory to setup the routes for the user api."""

    # TODO REBUILD THESE ROUTES

    #@app.route('/api/user/details', methods=['GET'])
    def get_user_details():
        """
        DEPRECATED

        api {get} /api/user/details UserGetDetails
        apiVersion 1.0.4
        apiName UserGetDetails
        apiGroup User
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
