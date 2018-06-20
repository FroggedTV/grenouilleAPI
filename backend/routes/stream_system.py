import logging

from flask import request, jsonify

from helpers import UrlImageToBase64
from models import User

def build_api_stream_system(app):
    """Factory to setup the routes for the stream system api."""

    @app.route('/api/obs/scenes/list', methods=['GET'])
    def get_obs_scene_list():
        """
        @api {get} /api/stream/obs/scenes/list OBSSceneList
        @apiVersion 1.0.4
        @apiName OBSSceneList
        @apiGroup StreamSystem
        @apiDescription List the available scenes in OBS.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiError (Errors){String} InternalOBSError Error communicating to OBS.
        @apiSuccess {String[]} scenes All available scenes with their name as Strings.
        """
        # Header checks
        header_key = request.headers.get('API_KEY', None)
        if header_key is None:
            return jsonify({'success': 'no',
                            'error': 'ApiKeyMissing',
                            'payload': {}
                            }), 200
        if header_key != app.config['API_KEY']:
            return jsonify({'success': 'no',
                            'error': 'ApiKeyInvalid',
                            'payload': {}
                            }), 200

        # TODO connect to obs

        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {
                        'scenes': []
                    }}), 200

    @app.route('/api/obs/scenes/list', methods=['GET'])
    def update_obs_scene():
        """
        @api {get} /api/stream/obs/scenes/list OBSSceneChange
        @apiVersion 1.0.4
        @apiName OBSSceneChange
        @apiGroup StreamSystem
        @apiDescription Change the OBS current scene to a new one

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiParam {String} scene Name of the scene to change to.
        @apiError (Errors){String} InternalOBSError Error communicating to OBS.
        @apiError (Errors){String} MissingScene The scene with the specified name doesn't exist.

        """
        # Header checks
        header_key = request.headers.get('API_KEY', None)
        if header_key is None:
            return jsonify({'success': 'no',
                            'error': 'ApiKeyMissing',
                            'payload': {}
                            }), 200
        if header_key != app.config['API_KEY']:
            return jsonify({'success': 'no',
                            'error': 'ApiKeyInvalid',
                            'payload': {}
                            }), 200

        # TODO connect to obs and do work

        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {}}), 200
