import logging

from flask import request, jsonify
from apiclient import discovery

from helpers.general import get_calendar_events, sanitize_events
from helpers.endpoint import secure
from helpers.image_gen import ImageGenerator

def build_api_calendar(app):
    """Factory to setup the routes for the calendar api."""

    @app.route('/api/calendar/generate', methods=['POST'])
    @secure(app, ['key', 'user'], ['calendar'])
    def post_calendar_generate(auth_token):
        """
        @api {post /api/calendar/generate CalendarGenerate
        @apiVersion 1.1.0
        @apiName CalendarGenerate
        @apiGroup Calendar
        @apiDescription Generate the calendar backgrounds.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.

        @apiError (Errors){String} GoogleCalendarError Impossible to get data events from GoogleCalendar.
        """

        ig = ImageGenerator(app)

        # Get events for frogged google calendar
        calendar_events = get_calendar_events(app.config['GOOGLE_API_KEY'],
                                              app.config['GOOGLE_CAL_FROGGED_ID'])
        if calendar_events is None:
            return jsonify({'success': 'no',
                            'error': 'GoogleCalendarError',
                            'payload': {}
                           }), 200
        ig.generate_froggedtv_calendar('now', sanitize_events(calendar_events[0], 10, 2))
        ig.generate_froggedtv_calendar('next', sanitize_events(calendar_events[1], 10, 2))

        # Get events for frogged google calendar
        calendar_events = get_calendar_events(app.config['GOOGLE_API_KEY'],
                                              app.config['GOOGLE_CAL_ARTIFACT_ID'])
        if calendar_events is None:
            return jsonify({'success': 'no',
                            'error': 'GoogleCalendarError',
                            'payload': {}
                            }), 200
        ig.generate_artifact_fr_calendar('now', sanitize_events(calendar_events[0], 10, 2))
        ig.generate_artifact_fr_calendar('next', sanitize_events(calendar_events[1], 10, 2))

        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                       }), 200
