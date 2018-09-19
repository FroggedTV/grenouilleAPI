import logging
from datetime import datetime, timedelta

from flask import request, jsonify
from apiclient import discovery

from helpers.general import safe_json_loads
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

        # Get events from google calendar
        calendar_events = [[], []]
        start_datetime = [datetime.now(), datetime.now()]
        end_datetime = [datetime.now(), datetime.now()]
        start_datetime[0] = start_datetime[0] - timedelta(days=start_datetime[0].weekday(),
                                                    hours=start_datetime[0].hour,
                                                    minutes=start_datetime[0].minute,
                                                    seconds=start_datetime[0].second,
                                                    microseconds=start_datetime[0].microsecond)

        start_datetime[1] = start_datetime[0] + timedelta(days=7)
        end_datetime[0] = start_datetime[0] + timedelta(days=7)
        end_datetime[1] = start_datetime[1] + timedelta(days=7)

        try:
            service = discovery.build('calendar', 'v3',
                                      developerKey=app.config['GOOGLE_API_KEY'],
                                      cache_discovery=False)

            for i in range(0, 2):
                events_result = service.events().list(calendarId=app.config['GOOGLE_CAL_ID'],
                                                      timeMin=start_datetime[i].isoformat() + 'Z',
                                                      maxResults=40,
                                                      singleEvents=True,
                                                      orderBy='startTime').execute()
                events = events_result.get('items', [])

                for event in events:
                    if 'dateTime' not in event['start'] or 'dateTime' not in event['end']:
                        continue
                    start = event['start'].get('dateTime')
                    start = datetime.strptime(''.join(start.rsplit(':', 1))[:18],
                                              "%Y-%m-%dT%H:%M:%S")
                    start.replace(tzinfo=None)
                    if start > end_datetime[i]:
                        continue
                    end = event['end'].get('dateTime')
                    end = datetime.strptime(''.join(end.rsplit(':', 1))[:18],
                                            "%Y-%m-%dT%H:%M:%S")
                    if start.hour < 10:
                        start=start.replace(hour=10, minute=0, second=0)
                    if end > end_datetime[i]:
                        end = end_datetime[i]
                    title = event['summary']
                    calendar_events[i].append({ 'start': start, 'end': end, 'title': title})
        except Exception as e:
            logging.exception(e)
            return jsonify({'success': 'no',
                            'error': 'GoogleCalendarError',
                            'payload': {}
                           }), 200

        # Generate image
        ig = ImageGenerator(app)
        ig.generate_calendar_image('calendar_now', calendar_events[0])
        ig.generate_calendar_image('calendar_next', calendar_events[1])
        return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}
                       }), 200
