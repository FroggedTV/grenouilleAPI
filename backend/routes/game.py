import logging
import collections

from flask import request, jsonify

from helpers import UrlImageToBase64
from models import db, Game, GameVIP

def build_api_game(app):
    """Factory to setup the routes for the Dota bots."""

    @app.route('/api/game/create', methods=['POST'])
    def create_game():
        """
        @api {post} /api/game/create GameCreate
        @apiVersion 1.0.0
        @apiName GameCreate
        @apiGroup DotaBots
        @apiDescription Queue a game to be host by bots.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiParam {Integer} team1 Id of the first team
        @apiParam {Integer[]} team1Ids SteamID (64bits) of first team players
        @apiParam {Integer} team2 Id of the second team
        @apiParam {Integer[]} team2Ids SteamID (64bits) of second team  players

        @apiError (Errors){String} MissingTeam1 team1 is not present.
        @apiError (Errors){String} InvalidTeam1 team1 is invalid.
        @apiError (Errors){String} MissingTeam1Ids team1Ids is not present.
        @apiError (Errors){String} InvalidTeam1Ids team1Ids is not an array of integers. Must be of len > 0.
        @apiError (Errors){String} MissingTeam2 team2 is not present.
        @apiError (Errors){String} InvalidTeam2 team2 is invalid.
        @apiError (Errors){String} MissingTeam2Ids team2Ids is not present.
        @apiError (Errors){String} InvalidTeam2Ids team2Ids is not an array of integers. Must be of len > 0.

        @apiParam {String[1..]} name Name of the game lobby.
        @apiError (Errors){String} MissingName name is not specified.
        @apiError (Errors){String} InvalidName name is not valid.
        @apiParam {String[1..]} password Password for the lobby.
        @apiError (Errors){String} MissingPassword password is not specified.
        @apiError (Errors){String} InvalidPassword password is not valid.
        @apiParam {Integer=1,2} teamChoosingFirst Team choosing 'side'/'pick order' first.
        @apiError (Errors){String} MissingTeamChoosingFirst teamChoosingFirst is not specified.
        @apiError (Errors){String} InvalidTeamChoosingFirst teamChoosingFirst is not valid.

        @apiSuccess {Integer} id Id of the game that will be hosted by bots.
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

        # team1 checks
        team1 = data.get('team1', None)
        if team1 is None:
            return jsonify({'success': 'no',
                            'error': 'MissingTeam1',
                            'payload': {}
                            }), 200
        if not isinstance(team1, int):
            return jsonify({'success': 'no',
                            'error': 'InvalidTeam1',
                            'payload': {}
                            }), 200

        # team2 checks
        team2 = data.get('team2', None)
        if team2 is None:
            return jsonify({'success': 'no',
                            'error': 'MissingTeam2',
                            'payload': {}
                            }), 200
        if not isinstance(team2, int):
            return jsonify({'success': 'no',
                            'error': 'InvalidTeam2',
                            'payload': {}
                            }), 200

        # team1Ids checks
        team1Ids = data.get('team1Ids', None)
        if team1Ids is None:
            return jsonify({'success': 'no',
                            'error': 'MissingTeam1Ids',
                            'payload': {}
                            }), 200
        if not isinstance(team1Ids, list) or len(team1Ids) == 0:
            return jsonify({'success': 'no',
                            'error': 'InvalidTeam1Ids',
                            'payload': {}
                            }), 200
        for id in team1Ids:
            if not isinstance(id, int):
                return jsonify({'success': 'no',
                                'error': 'InvalidTeam1Ids',
                                'payload': {}
                                }), 200

        # team2Ids checks
        team2Ids = data.get('team2Ids', None)
        if team2Ids is None:
            return jsonify({'success': 'no',
                            'error': 'MissingTeam2Ids',
                            'payload': {}
                            }), 200
        if not isinstance(team2Ids, list) or len(team2Ids) == 0:
            return jsonify({'success': 'no',
                            'error': 'InvalidTeam2Ids',
                            'payload': {}
                            }), 200
        for id in team2Ids:
            if not isinstance(id, int):
                return jsonify({'success': 'no',
                                'error': 'InvalidTeam2Ids',
                                'payload': {}
                                }), 200

        # name checks
        name = data.get('name', None)
        if name is None:
            return jsonify({'success': 'no',
                            'error': 'MissingName',
                            'payload': {}
                            }), 200
        if not isinstance(name, str):
            return jsonify({'success': 'no',
                            'error': 'InvalidName',
                            'payload': {}
                            }), 200
        if len(name) == 0:
            return jsonify({'success': 'no',
                            'error': 'InvalidName',
                            'payload': {}
                            }), 200

        # password checks
        password = data.get('password', None)
        if password is None:
            return jsonify({'success': 'no',
                            'error': 'MissingPassword',
                            'payload': {}
                            }), 200
        if not isinstance(password, str):
            return jsonify({'success': 'no',
                            'error': 'InvalidPassword',
                            'payload': {}
                            }), 200
        if len(password) == 0:
            return jsonify({'success': 'no',
                            'error': 'InvalidPassword',
                            'payload': {}
                            }), 200

        # teamChoosingFirst
        team_choosing_first = data.get('teamChoosingFirst', None)
        if team_choosing_first is None:
            return jsonify({'success': 'no',
                            'error': 'MissingTeamChoosingFirst',
                            'payload': {}
                            }), 200
        if not isinstance(team_choosing_first, int):
            return jsonify({'success': 'no',
                            'error': 'InvalidTeamChoosingFirst',
                            'payload': {}
                            }), 200
        if team_choosing_first not in [1, 2]:
            return jsonify({'success': 'no',
                            'error': 'InvalidTeamChoosingFirst',
                            'payload': {}
                            }), 200

        # Create game in database
        game = Game(name, password, team1, team2, team1Ids, team2Ids, team_choosing_first)
        db.session().add(game)
        db.session().commit()

        # Return ids
        return jsonify({'success': 'yes',
                        'payload': {
                            'id': game.id
                        }
                        }), 200

    @app.route('/api/game/details', methods=['GET'])
    def get_game_details():
        """
        @api {get} /api/game/details GameDetails
        @apiVersion 1.0.1
        @apiName GameDetails
        @apiGroup DotaBots
        @apiDescription Request game details.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiParam {Integer} id Id of the game hosted by bots.
        @apiError (Errors){String} MissingId Id is not present.
        @apiError (Errors){String} InvalidId Id is not an integer.
        @apiError (Errors){String} NoGameWithId Id is not present in database.

        @apiSuccess {Integer} id Id of the game hosted by bots.
        @apiSuccess {Integer} team1 Id of the first team
        @apiSuccess {Integer[]} team1Ids SteamID (64bits) of first team players
        @apiSuccess {Integer} team2 Id of the second team
        @apiSuccess {Integer[]} team2Ids SteamID (64bits) of second team  players
        @apiSuccess {String="GameStatus.WAITING_FOR_BOT", "GameStatus.CREATION_IN_PROGRESS",
         "GameStatus.WAITING_FOR_PLAYERS", "GameStatus.GAME_IN_PROGRESS", "GameStatus.COMPLETED",
         "GameStatus.CANCELLED"} status Game status.
        @apiSuccess {Integer=1,2} teamChoosingFirst Team choosing 'side'/'pick order' first
        @apiSuccess {String} bot Steam Bot managing the game (if status not 'GameStatus.WAITING_FOR_BOT')
        @apiSuccess {Integer} valveId Game Id in Valve database (if status 'GameStatus.COMPLETED')
        @apiSuccess {Integer=1,2} winner Team winning the game (if status 'GameStatus.COMPLETED')
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

        # id checks
        id = data.get('id', None)
        if id is None:
            return jsonify({'success': 'no',
                            'error': 'MissingId',
                            'payload': {}
                            }), 200
        if not isinstance(id, int):
            return jsonify({'success': 'no',
                            'error': 'InvalidId',
                            'payload': {}
                            }), 200
        game = db.session().query(Game).filter(Game.id==id).one_or_none()
        if game is None:
            return jsonify({'success': 'no',
                            'error': 'NoGameWithId',
                            'payload': {}
                            }), 200

        # Return details
        payload = {
            'id': game.id,
            'name': game.name,
            'password': game.password,
            'team1': game.team1,
            'team1Ids': game.team1_ids,
            'team2': game.team2,
            'team2Ids': game.team2_ids,
            'status': str(game.status),
            'teamChoosingFirst': game.team_choosing_first
        }
        if game.valve_id is not None:
            payload['valveId'] = game.valve_id
        if game.bot is not None:
            payload['bot'] = game.bot
        return jsonify({'success': 'yes',
                        'payload': payload
                        }), 200

    @app.route('/api/game/list', methods=['GET'])
    def list_game():
        """
        @api {get} /api/game/list GameList
        @apiVersion 1.0.2
        @apiName GameList
        @apiGroup DotaBots
        @apiDescription Get the list of multiple hosted games.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiParam {Integer{1-100}} [total=10] Optional number of entries to return.
        @apiError (Errors){String} InvalidTotal Total is not a positive integer.
        @apiParam {Integer{0-..}} [offset=0] Optional offset for database fetch.
        @apiError (Errors){String} InvalidOffset Offset is not a positive integer.
        @apiParam {String[]} [fields="['team1', 'team1Ids', 'team2', 'team2Ids', 'status', 'teamChoosingFirst', 'bot',
         'valveId', 'winner']"] Optional fields to return.
        @apiError (Errors){String} InvalidFields Fields is not an array.

        @apiSuccess {Object[]} games List of the Games ordered by decreasing id, with filters applied.
        @apiSuccess {Integer} games.id Id of the game hosted by bots.
        @apiSuccess {Integer} games.team1 Id of the first team
        @apiSuccess {Integer[]} games.team1Ids SteamID (64bits) of first team players
        @apiSuccess {Integer} games.team2 Id of the second team
        @apiSuccess {Integer[]} games.team2Ids SteamID (64bits) of second team  players
        @apiSuccess {String="GameStatus.WAITING_FOR_BOT", "GameStatus.CREATION_IN_PROGRESS",
         "GameStatus.WAITING_FOR_PLAYERS", "GameStatus.GAME_IN_PROGRESS", "GameStatus.COMPLETED",
         "GameStatus.CANCELLED"} games.status Game status.
        @apiSuccess {Integer=1,2} games.teamChoosingFirst Team choosing 'side'/'pick order' first
        @apiSuccess {String} games.bot Steam Bot managing the game (if status not 'GameStatus.WAITING_FOR_BOT')
        @apiSuccess {Integer} games.valveId Game Id in Valve database (if status 'GameStatus.COMPLETED')
        @apiSuccess {Integer=1,2} games.winner Team winning the game (if status 'GameStatus.COMPLETED')
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

        # TODO HERE
        payload = {}
        return jsonify({'success': 'no',
                        'payload': payload
                        }), 200

    @app.route('/api/game/vip/list', methods=['GET'])
    def list_game_vips():
        """
        @api {get} /api/game/vip/list GameVIPList
        @apiVersion 1.0.0
        @apiName GameVIPList
        @apiGroup DotaBots
        @apiDescription Get the list of all VIPs

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiSuccess {Object[]} vips List of the VIPs authorized in all games.
        @apiSuccess {Integer} vips.id Steam Id of the VIP.
        @apiSuccess {String="GameVIPType.CASTER","GameVIPType.ADMIN"} vips.type Type of the VIP.
        @apiSuccess {String} vips.name Name of the VIP.
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

        # Return ids
        vips = GameVIP.get_all_vips()
        return jsonify({'success': 'yes',
                        'payload': {'vips': vips}
                        }), 200

    @app.route('/api/game/vip/add', methods=['POST'])
    def add_game_vip():
        """
        @api {post} /api/game/vip/add GameVIPAdd
        @apiVersion 1.0.0
        @apiName GameVIPAdd
        @apiGroup DotaBots
        @apiDescription Add a new game VIP.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiParam {Integer} id SteamId (64bits) of the vip to add.
        @apiError (Errors){String} MissingId id is not specified.
        @apiError (Errors){String} InvalidId id is invalid.
        @apiError (Errors){String} VIPWithIdAlreadyExists VIP with id is already in database.

        @apiParam {String="CASTER","ADMIN"} type Type of the vip to add.
        @apiError (Errors){String} MissingType type is not specified.
        @apiError (Errors){String} InvalidType type is not valid.

        @apiParam {String[1..]} name Name of the vip to add.
        @apiError (Errors){String} MissingName name is not specified.
        @apiError (Errors){String} InvalidName name is not valid.
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

        # id checks
        id = data.get('id', None)
        if id is None:
            return jsonify({'success': 'no',
                            'error': 'MissingId',
                            'payload': {}
                            }), 200
        if not isinstance(id, int):
            return jsonify({'success': 'no',
                            'error': 'InvalidId',
                            'payload': {}
                            }), 200
        game_vip = db.session().query(GameVIP).filter(GameVIP.id==id).one_or_none()
        if game_vip is not None:
            return jsonify({'success': 'no',
                            'error': 'VIPWithIdAlreadyExists',
                            'payload': {}
                            }), 200

        # type checks
        type = data.get('type', None)
        if type is None:
            return jsonify({'success': 'no',
                            'error': 'MissingType',
                            'payload': {}
                            }), 200
        if not isinstance(type, str) or (type not in ['CASTER', 'ADMIN']):
            return jsonify({'success': 'no',
                            'error': 'InvalidType',
                            'payload': {}
                            }), 200

        # name checks
        name = data.get('name', None)
        if name is None:
            return jsonify({'success': 'no',
                            'error': 'MissingName',
                            'payload': {}
                            }), 200
        if not isinstance(name, str):
            return jsonify({'success': 'no',
                            'error': 'InvalidName',
                            'payload': {}
                            }), 200
        if len(name) == 0:
            return jsonify({'success': 'no',
                            'error': 'InvalidName',
                            'payload': {}
                            }), 200

        # Add VIP
        game_vip = GameVIP(id, type, name)
        db.session().add(game_vip)
        db.session().commit()

        return jsonify({'success': 'yes',
                        'payload': {}
                        }), 200

    @app.route('/api/game/vip/remove', methods=['POST'])
    def remove_game_vip():
        """
        @api {post} /api/game/vip/remove GameVIPRemove
        @apiVersion 1.0.0
        @apiName GameVIPRemove
        @apiGroup DotaBots
        @apiDescription Remove a game VIP.

        @apiHeader {String} API_KEY Restricted API_KEY necessary to call the endpoint.
        @apiError (Errors){String} ApiKeyMissing Missing API_KEY header.
        @apiError (Errors){String} ApiKeyInvalid Invalid API_KEY header.

        @apiParam {Integer} id SteamId of the vip to remove.
        @apiError (Errors){String} MissingId id is not specified.
        @apiError (Errors){String} InvalidId id is invalid.
        @apiError (Errors){String} VIPDoesNotExist VIP with id does not exist in the database.
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

        # id checks
        id = data.get('id', None)
        if id is None:
            return jsonify({'success': 'no',
                            'error': 'MissingId',
                            'payload': {}
                            }), 200
        if not isinstance(id, int):
            return jsonify({'success': 'no',
                            'error': 'InvalidId',
                            'payload': {}
                            }), 200
        game_vip = db.session().query(GameVIP).filter(GameVIP.id==id).one_or_none()
        if game_vip is None:
            return jsonify({'success': 'no',
                            'error': 'VIPDoesNotExist',
                            'payload': {}
                            }), 200

        # Remove VIP
        db.session().delete(game_vip)
        db.session().commit()

        return jsonify({'success': 'yes',
                        'payload': {}
                        }), 200
