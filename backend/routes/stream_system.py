import logging

from flask import request, jsonify

from helpers import send_command_to_obs, url_image_to_base64
from models import User

def build_api_stream_system(app):
    """Factory to setup the routes for the stream system api."""

    @app.route('/api/obs/scene/list', methods=['GET'])
    def get_obs_scene_list():
        """
        @api {get} /api/obs/scene/list OBSSceneList
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

        return jsonify({'success': 'no',
                    'error': 'NotImplementedError',
                    'payload': {

                    }}), 200

    @app.route('/api/obs/scene/update', methods=['POST'])
    def update_obs_scene():
        """
        @api {post} /api/obs/scene/update OBSSceneUpdate
        @apiVersion 1.0.4
        @apiName OBSSceneUpdate
        @apiGroup StreamSystem
        @apiDescription Change the OBS current scene to a new one

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiParam {String} scene Name of the scene to change to.
        @apiError (Errors){String} InternalOBSError Error communicating to OBS.
        @apiError (Errors){String} MissingSceneParameter Scene is not present in the parameters.
        @apiError (Errors){String} InvalidSceneParameter Scene is not valid String.
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

        data = request.get_json(force=True)

        # scene checks
        scene = data.get('scene', None)
        if scene is None:
            return jsonify({'success': 'no',
                            'error': 'MissingSceneParameter',
                            'payload': {}
                            }), 200
        if not isinstance(scene, str):
            return jsonify({'success': 'no',
                            'error': 'InvalidSceneParameter',
                            'payload': {}
                            }), 200
        if len(scene) == 0:
            return jsonify({'success': 'no',
                            'error': 'InvalidSceneParameter',
                            'payload': {}
                            }), 200

        # Send command to obs
        try:
            result = send_command_to_obs('SetCurrentScene', {'scene-name': scene})
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {}}), 200

    @app.route('/api/obs/record/start', methods=['POST'])
    def get_obs_record_start():
        """
        @api {post} /api/obs/record/start OBSRecordStart
        @apiVersion 1.0.5
        @apiName OBSRecordStart
        @apiGroup StreamSystem
        @apiDescription Start the recording by OBS.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiError (Errors){String} InternalOBSError Error communicating to OBS.
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

        # Send command to obs
        try:
            result = send_command_to_obs('StartRecording', {})
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {}}), 200

    @app.route('/api/obs/record/stop', methods=['POST'])
    def get_obs_record_stop():
        """
        @api {post} /api/obs/record/stop OBSRecordStop
        @apiVersion 1.0.5
        @apiName OBSRecordStop
        @apiGroup StreamSystem
        @apiDescription Stop the recording by OBS.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiError (Errors){String} InternalOBSError Error communicating to OBS.
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

        # Send command to obs
        try:
            result = send_command_to_obs('StopRecording', {})
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {}}), 200
