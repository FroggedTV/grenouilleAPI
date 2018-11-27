import logging
import os

from flask import request, jsonify, send_file
from apiclient import discovery

from helpers.general import get_calendar_events, sanitize_events
from helpers.endpoint import secure, has_client_scope
from helpers.image_gen import ImageGenerator

from database import db
from models.Stream import Stream

def build_api_calendar(app):
    """Factory to setup the routes for the calendar api."""

    ig = ImageGenerator(app)

    @app.route('/api/calendar/generate', methods=['POST'])
    @secure(app)
    def post_calendar_generate(auth_token):
        """
        @api {post /api/calendar/generate CalendarGenerate
        @apiVersion 1.2.0
        @apiName CalendarGenerate
        @apiGroup Calendar
        @apiDescription Generate the calendar backgrounds.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiParam {String} channel Channel to generate the calendar for.
        @apiError (Errors){String} ChannelParameterMissing Channel is not present in the parameters.
        @apiError (Errors){String} ChannelParameterInvalid Channel is not a valid String.
        @apiError (Errors){String} NoCalendarInformationInDatabase Google calendar id is not setup inside the database.
        @apiError (Errors){String} GoogleCalendarError Impossible to get data events from GoogleCalendar.
        """
        data = request.get_json(force=True)

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
        if not has_client_scope(auth_token, channel, ['calendar']):
            return jsonify({'success': 'no', 'error': 'ClientAccessRefused', 'payload': {}}), 403

        # Get calendar information from database
        stream = Stream.get(channel)
        if stream is None or stream.google_calendar_id is None:
            return jsonify({'success': 'no',
                            'error': 'NoCalendarInformationInDatabase',
                            'payload': {}
                            }), 200

        # Get events for the calendar
        calendar_events = get_calendar_events(app.config['GOOGLE_API_KEY'], stream.google_calendar_id)
        if calendar_events is None:
            return jsonify({'success': 'no',
                            'error': 'GoogleCalendarError',
                            'payload': {}
                           }), 200

        ig.generate_calendar(stream.id, 'current', '10h2h', sanitize_events(calendar_events[0], 10, 2))
        ig.generate_calendar(stream.id, 'next', '10h2h', sanitize_events(calendar_events[1], 10, 2))
        ig.generate_calendar(stream.id, 'current', '0h0h', sanitize_events(calendar_events[0], 0, 0))
        ig.generate_calendar(stream.id, 'next', '0h0h', sanitize_events(calendar_events[1], 0, 0))

        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                       }), 200

    @app.route('/api/calendar/img/<name>', methods=['GET'])
    def get_calendar_img(name):
        path_file = os.path.join(app.config['IMG_GENERATE_PATH'], name)
        if not os.path.isfile(path_file):
            return send_file('static/img/1080p_default.jpg')
        else:
            return send_file(path_file)
