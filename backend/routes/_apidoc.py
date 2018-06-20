#########################################################
#########################################################
## OLD ROUTE API VERSIONS FOR DOCUMENTATION GENERATION ##
#########################################################
#########################################################

##################
# Authentication #
##################

"""
@api {get} /api/auth/login 1.1 - Get a Refresh Token with Steam Login
@apiVersion 1.0.0
@apiName RefreshTokenGet
@apiGroup Authentication
@apiDescription Calling this endpoint redirects to the steam login page.
After login, the user is redirected to a callback url with the refresh token as a parameter.
The URL is defined in the backend config.
"""

"""
@api {get} /api/auth/token 2 - Get a Auth Token from a Refresh Token
@apiVersion 1.0.0
@apiName AuthTokenGet
@apiGroup Authentication
@apiDescription Refresh tokens are long lived but auth tokens are short lived.
Using a valid refresh token, this api delivers an auth token to access data endpoints.
@apiHeader {String} Authorization 'Bearer <refresh_token>'
@apiSuccess {String} auth_token Authentication token short lived to access data.
@apiError (Errors){String} InvalidHeader Authorization header not well formated.
@apiError (Errors){String} NoRefreshToken There is no refresh token provided.
@apiError (Errors){String} ExpiredRefreshToken Refresh token has expired and user should log again.
@apiError (Errors){String} InvalidRefreshToken Token is invalid (decode, rights, signature...).
"""

############
# DotaBots #
############

"""
@api {get} /api/game/details GameGetDetails
@apiVersion 1.0.0
@apiName GameGetDetails
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
