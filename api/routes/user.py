import logging

from flask import jsonify

def build_api_user(app):
    """Factory to setup the routes for the user api."""

    @app.route('/api/user/hello', methods=['GET'])
    def hello():
        """Test Method

        Args:
            xx
        """
        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {'user': 'toto'}}), 200
