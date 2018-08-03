import logging
import csv
import os
from io import StringIO

from flask import request, jsonify, send_file
from models import db, CSVData, DynamicConfiguration

from helpers.general import safe_json_loads
from helpers.endpoint import secure
from helpers.image_gen import ImageGenerator

def build_api_stats(app):
    """Factory to setup the routes for the stats api."""

    ig = ImageGenerator(app)

    @app.route('/api/stats/csv/get', methods=['GET'])
    @secure(app, ['key', 'user'], ['stats_manage'])
    def get_stats_csv(auth_token):
        """
        @api {get} /api/stats/csv/get StatsCSVGet
        @apiVersion 1.1.0
        @apiName StatsCSVGet
        @apiGroup Stats
        @apiDescription Get CSV saved for stats.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} key CSV key to get.
        @apiError (Errors){String} KeyInvalid key is not a valid string.
        @apiError (Errors){String} KeyDataDoesntExist key has no data associated.

        @apiSuccess {Number} csv CSVData associated to the key.
        """
        data = safe_json_loads(request.args.get('data', '{}'))

        # key check
        key = data.get('key', 10)
        if not isinstance(key, str) or len(key) <= 0:
            return jsonify({'success': 'no',
                            'error': 'KeyInvalid',
                            'payload': {}
                            }), 200

        csv_data = db.session.query(CSVData).filter(CSVData.key==key).one_or_none()
        if csv_data is None:
            return jsonify({'success': 'no',
                            'error': 'KeyDataDoesntExist',
                            'payload': {}
                            }), 200
        else:
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {
                                'csv': csv_data.value
                            }
                            }), 200

    @app.route('/api/stats/csv/update', methods=['POST'])
    @secure(app, ['key', 'user'], ['stats_manage'])
    def post_stats_csv(auth_token):
        """
        @api {get} /api/stats/csv/update StatsCSVUpdate
        @apiVersion 1.1.0
        @apiName StatsCSVUpdate
        @apiGroup Stats
        @apiDescription Update CSV saved for stats.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} key CSV key to get.
        @apiError (Errors){String} KeyInvalid key is not a valid string.

        @apiParam {String} value CSV data.
        @apiError (Errors){String} ValueInvalid value is not a valid string.
        @apiError (Errors){String} ValueCSVInvalid value CSV is not a valid same length column csv.
        """
        data = request.get_json(force=True)

        # key check
        key = data.get('key', 10)
        if not isinstance(key, str) or len(key) <= 0:
            return jsonify({'success': 'no',
                            'error': 'KeyInvalid',
                            'payload': {}
                            }), 200

        # value check
        value = data.get('value', 10)
        if not isinstance(value, str) or len(value) <= 0:
            return jsonify({'success': 'no',
                            'error': 'ValueInvalid',
                            'payload': {}
                            }), 200

        columns = None
        for row in csv.reader(StringIO(value), delimiter=','):
            if columns is None:
                columns = len(row)
            else:
                if len(row) != columns:
                    return jsonify({'success': 'no',
                                    'error': 'ValueCSVInvalid',
                                    'payload': {}
                                    }), 200

        CSVData.upsert(key, value)
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200

    @app.route('/api/stats/img/<name>', methods=['GET'])
    def get_stats_img(name):
        path_file = os.path.join(app.config['IMG_GENERATE_PATH'], name + '.png')
        if not os.path.isfile(path_file):
            return send_file('static/img/stats_default.jpg')
        else:
            return send_file(path_file)

    @app.route('/api/stats/csv/img/generate', methods=['POST'])
    @secure(app, ['key', 'user'], ['stats_manage'])
    def post_stats_img_generate(auth_token):
        """
        @api {get} /api/stats/img/generate StatsCSVGenerateIMG
        @apiVersion 1.1.0
        @apiName StatsCSVGenerateIMG
        @apiGroup Stats
        @apiDescription Start the generation of CSV image.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} key CSV key to generate.
        @apiError (Errors){String} KeyInvalid key is not a valid string.
        @apiError (Errors){String} KeyDataDoesntExist key has no data associated.

        @apiParam {Number} [team_id] Optional team id to refine the generation with.
        @apiError (Errors){String} TeamIdInvalid key is not a valid string.
        @apiParam {Number} [player_id] Optional player id to refine the generation with.
        @apiError (Errors){String} PlayerIdInvalid key is not a valid string.
        """
        data = request.get_json(force=True)

        # key check
        key = data.get('key', 10)
        if not isinstance(key, str) or len(key) <= 0:
            return jsonify({'success': 'no',
                            'error': 'KeyInvalid',
                            'payload': {}
                            }), 200

        csv_data = db.session.query(CSVData).filter(CSVData.key==key).one_or_none()
        if csv_data is None:
            return jsonify({'success': 'no',
                            'error': 'KeyDataDoesntExist',
                            'payload': {}
                            }), 200

        # Optional parameters check
        team_id = data.get('team_id', '0')
        if len(team_id) == 0 or not team_id.isdigit():
            return jsonify({'success': 'no',
                            'error': 'TeamIdInvalid',
                            'payload': {}
                            }), 200
        team_id = int(team_id)
        if team_id < 0:
            return jsonify({'success': 'no',
                            'error': 'TeamIdInvalid',
                            'payload': {}
                            }), 200
        elif team_id == 0:
            team_id = None

        player_id = data.get('player_id', '0')
        if len(player_id) == 0 or not player_id.isdigit():
            return jsonify({'success': 'no',
                            'error': 'PlayerIdInvalid',
                            'payload': {}
                            }), 200
        player_id = int(player_id)
        if player_id < 0:
            return jsonify({'success': 'no',
                            'error': 'PlayerIdInvalid',
                            'payload': {}
                            }), 200
        elif player_id == 0:
            player_id = None

        # Generate
        ig.generate_csv_image(key, team_id, player_id)
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                        }), 200

    @app.route('/api/stats/scene/status/get', methods=['GET'])
    @secure(app, ['key', 'user'], ['stats_manage_scene'])
    def get_stats_scene_status(auth_token):
        """
        @api {get} /api/stats/scene/status/get StatsSceneStatusGet
        @apiVersion 1.1.0
        @apiName StatsSceneStatusGet
        @apiGroup Stats
        @apiDescription Get the status of the stat scene.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiSuccess {Boolean} activated Boolean to show if the stat scene is activated or disabled.
        """

        stats_scene_status_dc = db.session.query(DynamicConfiguration).filter(DynamicConfiguration.key=='stats_scene_status').one_or_none()
        if stats_scene_status_dc is None:
            stats_scene_status = 'False'
        else:
            stats_scene_status = stats_scene_status_dc.value

        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {
                            'activated': stats_scene_status == 'True'
                        }
                        }), 200

    @app.route('/api/stats/scene/status/update', methods=['POST'])
    @secure(app, ['key', 'user'], ['stats_manage_scene'])
    def post_stats_scene_status(auth_token):
        """
        @api {get} /api/stats/scene/status/update StatsSceneStatusUpdate
        @apiVersion 1.1.0
        @apiName StatsSceneStatusUpdate
        @apiGroup Stats
        @apiDescription Update the status of the stat scene.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {Boolean} activated New value of the stat scene status.
        @apiError (Errors){String} ActivatedInvalid activated is not a valid boolean.

        @apiSuccess {Boolean} activated Boolean to show if the stat scene is activated or disabled.
        """
        data = request.get_json(force=True)

        # activated check
        activated = data.get('activated', False)
        if not isinstance(activated, bool):
            return jsonify({'success': 'no',
                            'error': 'ActivatedInvalid',
                            'payload': {}
                            }), 200

        # change scene status
        stats_scene_status_dc = db.session.query(DynamicConfiguration).filter(DynamicConfiguration.key=='stats_scene_status').one_or_none()
        if stats_scene_status_dc is None:
            stats_scene_status_dc = DynamicConfiguration('stats_scene_status', str(activated))
            db.session.add(stats_scene_status_dc)
        else:
            stats_scene_status_dc.value = str(activated)
        db.session.commit()

        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {
                            'activated': stats_scene_status_dc.value == 'True'
                        }
                        }), 200


    @app.route('/api/stats/scene/get', methods=['GET'])
    def get_stats_scene():
        """
        @api {get} /api/stats/scene/get StatsSceneGet
        @apiVersion 1.1.0
        @apiName StatsSceneGet
        @apiGroup Stats
        @apiDescription Get the stat image.

        @apiSuccess {String} img Image to use in the stat scene.
        @apiSuccess {String} last_modified Last time the file was modified.
        @apiSuccess {Boolean} continue Should the stat scene user continue.
        """
        stats_scene_dc = db.session.query(DynamicConfiguration).filter(DynamicConfiguration.key=='stats_scene').one_or_none()
        if stats_scene_dc is None:
            stats_scene = 'empty'
        else:
            stats_scene = stats_scene_dc.value
        db.session.commit()

        path_file = os.path.join(app.config['IMG_GENERATE_PATH'], stats_scene + '.png')
        if not os.path.isfile(path_file):
            last_modified = ''
        else:
            last_modified = os.path.getmtime(path_file)

        # Give status inside
        stats_scene_status_dc = db.session.query(DynamicConfiguration).filter(DynamicConfiguration.key=='stats_scene_status').one_or_none()
        if stats_scene_status_dc is None:
            stats_scene_status = 'False'
        else:
            stats_scene_status = stats_scene_status_dc.value

        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {
                            'continue': stats_scene_status == 'True',
                            'img': stats_scene,
                            'last_modified': last_modified
                        }
                        }), 200

    @app.route('/api/stats/scene/update', methods=['POST'])
    @secure(app, ['key', 'user'], ['stats_manage_scene'])
    def post_stats_scene(auth_token):
        """
        @api {get} /api/stats/scene/update StatsSceneUpdate
        @apiVersion 1.1.0
        @apiName StatsSceneUpdate
        @apiGroup Stats
        @apiDescription Update the stat scene.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} img New scene.
        @apiError (Errors){String} ImgInvalid img is not a valid string.
        @apiError (Errors){String} ImgNoFile img is not a valid file image.

        @apiSuccess {String} img Image to show appended with a cache bang.
        @apiSuccess {String} last_modified Last time the file was modified.
        """
        data = request.get_json(force=True)

        # activated check
        img = data.get('img', '')
        if not isinstance(img, str) or len(img) <= 0:
            return jsonify({'success': 'no',
                            'error': 'ImgInvalid',
                            'payload': {}
                            }), 200

        # change scene
        stats_scene_status_dc = db.session.query(DynamicConfiguration).filter(DynamicConfiguration.key=='stats_scene').one_or_none()
        if stats_scene_status_dc is None:
            stats_scene_status_dc = DynamicConfiguration('stats_scene', img)
            db.session.add(stats_scene_status_dc)

        # File look on disk
        path_file = os.path.join(app.config['IMG_GENERATE_PATH'], img + '.png')
        if not os.path.isfile(path_file):
            return jsonify({'success': 'no',
                            'error': 'ImgNoFile',
                            'payload': {}
                            }), 200

        last_modified = os.path.getmtime(path_file)
        stats_scene_status_dc.value = img
        db.session.commit()

        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {
                            'img': stats_scene_status_dc.value,
                            'last_modified': last_modified
                        }
                        }), 200
