import logging

from flask import request, jsonify
from models import User

from helpers.endpoint import secure

def build_api_user(app):
    """Factory to setup the routes for the user api."""

    @app.route('/api/user/me/details', methods=['GET'])
    @secure(app, ['user'], [])
    def get_user_me_details(auth_token):
        """
        @api {get} /api/user/me/details UserMeDetails
        @apiVersion 1.1.1
        @apiName UserMeDetails
        @apiGroup User
        @apiDescription Get detailed information of myself, scopes, id...

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.

        @apiSuccess {Integer} steam_id Steam ID of the user.
        @apiSuccess {String[]} scopes List of scopes this user has access to.
        """
        return jsonify({'success': 'yes',
                    'error': '',
                    'payload': {
                        'steam_id': auth_token['client']['steamid'],
                        'scopes': auth_token['client']['scopes']
                    }}), 200
