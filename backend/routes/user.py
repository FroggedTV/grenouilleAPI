import logging

from flask import jsonify

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

        @apiSuccess {String} id SteamID (64bits)
        @apiSuccess {String} nickname Username

        @apiError (Errors){String} UserNotFound There is no user in the database with this id.
        """
        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {'user': 'toto'}}), 200
