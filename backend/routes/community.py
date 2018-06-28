import logging

from flask import request, jsonify

from helpers import UrlImageToBase64
from models import User

def build_api_community(app):
    """Factory to setup the routes for the community api."""

    @app.route('/api/calendar/get', methods=['GET'])
    def get_calendar():
        """
        @api {get} /api/calendar/get CalendarGet
        @apiVersion 1.0.4
        @apiName CalendarGet
        @apiGroup Community
        @apiDescription This method returns the streaming calendar from the FroggedTV Google calendar.
        Calendar is updated every hour with a cron job, or forced by an API call.

        @apiSuccess {Object[]} calendar events available into the calendar for the current week.
        @apiSuccess {String} calendar.title Title of the event.
        """
        # TODO
        logging.error('TODO: NOT IMPLEMENTED')
        return jsonify({'success': 'no',
                    'error': 'NotImplementedError',
                    'payload': {

                    }}), 200


    @app.route('/api/calendar/get', methods=['GET'])
    def update_calendar():
        """
        @api {get} /api/calendar/update CalendarUpdate
        @apiVersion 1.0.4
        @apiName CalendarUpdate
        @apiGroup Community
        @apiDescription Force internal calendar update from google doc.
        """
        # TODO
        logging.error('TODO: NOT IMPLEMENTED')
        return jsonify({'success': 'no',
                    'error': 'NotImplementedError',
                    'payload': {

                    }}), 200
