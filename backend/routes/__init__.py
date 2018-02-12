# OLD ROUTE API VERSIONS FOR DOCUMENTATION GENERATION

"""
@api {get} /api/game/details GameDetails
@apiVersion 1.0.0
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
@apiSuccess {String} name Name of the game lobby.
@apiSuccess {String} password Password for the lobby.
@apiSuccess {Integer[]} team1Ids SteamID (64bits) of first team players
@apiSuccess {Integer} team2 Id of the second team
@apiSuccess {Integer[]} team2Ids SteamID (64bits) of second team  players
@apiSuccess {String="GameStatus.WAITING_FOR_BOT", "GameStatus.CREATION_IN_PROGRESS",
 "GameStatus.WAITING_FOR_PLAYERS", "GameStatus.GAME_IN_PROGRESS", "GameStatus.COMPLETED",
 "GameStatus.CANCELLED"} status Game status.
@apiSuccess {Integer=1,2} teamChoosingFirst Team choosing 'side'/'pick order' first
@apiSuccess {Integer} valveId Game Id in Valve database (if status 'GameStatus.COMPLETED')
@apiSuccess {Integer=1,2} winner Team winning the game (if status 'GameStatus.COMPLETED')
"""
