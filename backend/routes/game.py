import logging

from flask import request, jsonify

from helpers import UrlImageToBase64
from models import User

def build_api_game(app):
    """Factory to setup the routes for the Dota bots."""

    @app.route('/api/game/host', methods=['POST'])
    def host_game():
        """
        @api {get} /api/game/host HostGame
        @apiName HostGame
        @apiGroup Game
        @apiDescription Queue a game to host by bots.

        @apiHeader {String} API-KEY <Restricted API-KEY necessary to call the endpoint>
        @apiError (Errors){String} KeyError Missing or invalid API-KEY header.

        @apiParam {String} team1Ids SteamID (64bits) of first team players, separated by ','
        @apiParam {String} team2Ids SteamID (64bits) of second team  players, separated by ','
        @apiParam {String} spectatorIds SteamID (64bits) of spectator players, separated by ',' (Optional)
        @apiParam {String} team1 Name of the first team
        @apiParam {String} team2 Name of the second team

        @apiSuccess {String} hostId Id of the game hosted by bots for further requests.

        @apiError (Errors){String} MissingTeam1IdsParameter team1Ids is not present.
        @apiError (Errors){String} InvalidTeam1IdsParameter team1Ids is not a list of steamIds.
        @apiError (Errors){String} MissingTeam2IdsParameter team2Ids is not present.
        @apiError (Errors){String} InvalidTeam2IdsParameter team2Ids is not a list of steamIds.
        @apiError (Errors){String} MissingTeam1Parameter team1 is not present.
        @apiError (Errors){String} MissingTeam2Parameter team2 is not present.
        """

        return jsonify({'success': 'no',
                        'error': 'KeyError',
                        'payload': {}
                        }), 200
