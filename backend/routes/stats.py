import logging
import csv
import os
from io import StringIO

from flask import request, jsonify, send_file
from models import db, CSVData

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
        else:
            ig.generate_csv_image(key)
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {}
                            }), 200

