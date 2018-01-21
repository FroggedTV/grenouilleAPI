import logging

from flask import request, jsonify

from helpers import UrlImageToBase64
from models import User

def build_api_game(app):
    """Factory to setup the routes for the Dota bots."""

    @app.route('/api/game/host', methods=['POST'])
    def host_game():
        """
        @api {post} /api/game/host HostGame
        @apiName HostGame
        @apiGroup Game
        @apiDescription Queue a game to host by bots.

        @apiHeader {String} API-KEY Restricted API-KEY necessary to call the endpoint.
        @apiError (Errors){String} KeyError Missing or invalid API-KEY header.

        @apiParam {String} team1 Name of the first team
        @apiParam {String} team1Ids SteamID (64bits) of first team players, separated by ','
        @apiParam {String} team2 Name of the second team
        @apiParam {String} team2Ids SteamID (64bits) of second team  players, separated by ','
        @apiParam {String} spectatorIds SteamID (64bits) of spectator players, separated by ',' (Optional)

        @apiSuccess {String} hostId Id of the game hosted by bots for further requests.

        @apiError (Errors){String} MissingTeam1Parameter team1 is not present.
        @apiError (Errors){String} MissingTeam1IdsParameter team1Ids is not present.
        @apiError (Errors){String} InvalidTeam1IdsParameter team1Ids is not a list of steamIds.
        @apiError (Errors){String} MissingTeam2Parameter team2 is not present.
        @apiError (Errors){String} MissingTeam2IdsParameter team2Ids is not present.
        @apiError (Errors){String} InvalidTeam2IdsParameter team2Ids is not a list of steamIds.
        """
        header_key = request.headers.get('API-KEY', None)
        if header_key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyError',
                            'payload': {}
                            }), 200

        return jsonify({'success': 'no',
                        'error': 'KeyError',
                        'payload': {}
                        }), 200

    @app.route('/api/game/details', methods=['GET'])
    def details_game():
        """
        @api {get} /api/game/details GameDetails
        @apiName GameDetails
        @apiGroup Game
        @apiDescription Request game details.

        @apiHeader {String} API-KEY Restricted API-KEY necessary to call the endpoint.
        @apiError (Errors){String} KeyError Missing or invalid API-KEY header.

        @apiParam {String} hostId Id of the game hosted by bots.

        @apiSuccess {String} hostId Id of the game hosted by bots.
        @apiSuccess {String} team1 Name of the first team
        @apiSuccess {String} team1Ids SteamID (64bits) of first team players, separated by ','
        @apiSuccess {String} team2 Name of the second team
        @apiSuccess {String} team2Ids SteamID (64bits) of second team  players, separated by ','
        @apiSuccess {String} spectatorIds SteamID (64bits) of spectator players, separated by ',' (Optional)
        @apiSuccess {String} status Game status. Possible values are 'waiting bot', 'creation in progress',
        'waiting for players', 'game in progress', 'completed', 'canceled'.
        @apiSuccess {String} valveId Game Id in Valve database.
        @apiSuccess {String} coinTossWinner Winner of the coin toss: 'team1' or 'team2'.
        @apiSuccess {String} team1Choice Choice after the coin toss for team1: 'fp', 'sp', 'radiant' or 'dire'
        @apiSuccess {String} team2Choice Choice after the coin toss for team2: 'fp', 'sp', 'radiant' or 'dire'
        @apiSuccess {String} winner Winner of the game: 'team1' or 'team2'.
        @apiSuccess {Integer} team1NoJoin Number of players who didn't join the lobby from team1.
        @apiSuccess {Integer} team2NoJoin Number of players who didn't join the lobby from team2.

        @apiSuccess {String} hostId Id of the game hosted by bots for further requests.

        @apiError (Errors){String} MissingHostIdParameter hostId is not present.
        @apiError (Errors){String} InvalidHostIdParameter hostId is not a valid id or not present.
        """
        header_key = request.headers.get('API-KEY', None)
        if header_key is None:
            return jsonify({'success': 'no',
                            'error': 'KeyError',
                            'payload': {}
                            }), 200

        return jsonify({'success': 'no',
                        'error': 'KeyError',
                        'payload': {}
                        }), 200
