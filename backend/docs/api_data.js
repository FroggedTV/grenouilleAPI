define({ "api": [
  {
    "type": "get",
    "url": "/api/auth/token",
    "title": "AuthTokenGet",
    "version": "1.0.4",
    "name": "AuthTokenGet",
    "group": "Authentication",
    "description": "<p>Refresh tokens are long lived but auth tokens are short lived. Using a valid refresh token, this api delivers an auth token to access data endpoints.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;refresh_token&gt;'</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "auth_token",
            "description": "<p>Authentication token short lived to access data.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidHeader",
            "description": "<p>Authorization header not well formated.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "NoRefreshToken",
            "description": "<p>There is no refresh token provided.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ExpiredRefreshToken",
            "description": "<p>Refresh token has expired and user should log again.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidRefreshToken",
            "description": "<p>Token is invalid (decode, rights, signature...).</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/token",
    "title": "2 - Get a Auth Token from a Refresh Token",
    "version": "1.0.0",
    "name": "AuthTokenGet",
    "group": "Authentication",
    "description": "<p>Refresh tokens are long lived but auth tokens are short lived. Using a valid refresh token, this api delivers an auth token to access data endpoints.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;refresh_token&gt;'</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "auth_token",
            "description": "<p>Authentication token short lived to access data.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidHeader",
            "description": "<p>Authorization header not well formated.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "NoRefreshToken",
            "description": "<p>There is no refresh token provided.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ExpiredRefreshToken",
            "description": "<p>Refresh token has expired and user should log again.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidRefreshToken",
            "description": "<p>Token is invalid (decode, rights, signature...).</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/_apidoc.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/login",
    "title": "RefreshTokenGet",
    "version": "1.0.4",
    "name": "RefreshTokenGet",
    "group": "Authentication",
    "description": "<p>First endpoint to call in the auth process. Calling it redirects to the steam login page. After login, the user is redirected to a callback url with the refresh token as a parameter. The URL is defined in the backend config. Frontend must be able to manage the token incoming as a parameter.</p>",
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/login",
    "title": "1.1 - Get a Refresh Token with Steam Login",
    "version": "1.0.0",
    "name": "RefreshTokenGet",
    "group": "Authentication",
    "description": "<p>Calling this endpoint redirects to the steam login page. After login, the user is redirected to a callback url with the refresh token as a parameter. The URL is defined in the backend config.</p>",
    "filename": "backend/routes/_apidoc.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/calendar/get",
    "title": "CalendarGet",
    "version": "1.0.4",
    "name": "CalendarGet",
    "group": "Community",
    "description": "<p>This method returns the streaming calendar from the FroggedTV Google calendar. Calendar is updated every hour with a cron job, or forced by an API call.</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "calendar",
            "description": "<p>events available into the calendar for the current week.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "calendar.title",
            "description": "<p>Title of the event.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/community.py",
    "groupTitle": "Community"
  },
  {
    "type": "get",
    "url": "/api/calendar/update",
    "title": "CalendarUpdate",
    "version": "1.0.4",
    "name": "CalendarUpdate",
    "group": "Community",
    "description": "<p>Force internal calendar update from google doc.</p>",
    "filename": "backend/routes/community.py",
    "groupTitle": "Community"
  },
  {
    "type": "get",
    "url": "/api/game/bot/pause/get",
    "title": "BotPauseGet",
    "version": "1.0.3",
    "name": "BotPauseGet",
    "group": "DotaBots",
    "description": "<p>Get the bot pause status</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "BotPauseMissing",
            "description": "<p>Bot pause was never set, default value is 'False'.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "allowedValues": [
              "True",
              "False"
            ],
            "optional": false,
            "field": "bot_pause",
            "description": "<p>Pause status of the bot.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/game.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "post",
    "url": "/api/game/bot/pause/update",
    "title": "BotPauseUpdate",
    "version": "1.0.3",
    "name": "BotPauseUpdate",
    "group": "DotaBots",
    "description": "<p>Update the bot pause status.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingBotPause",
            "description": "<p>bot_pause is not specified.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidBotPause",
            "description": "<p>bot_pause is invalid.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "True",
              "False"
            ],
            "optional": false,
            "field": "bot_pause",
            "description": "<p>Pause status of the bot.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "allowedValues": [
              "True",
              "False"
            ],
            "optional": false,
            "field": "bot_pause",
            "description": "<p>Pause status of the bot after update.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/game.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "post",
    "url": "/api/game/create",
    "title": "GameCreate",
    "version": "1.0.0",
    "name": "GameCreate",
    "group": "DotaBots",
    "description": "<p>Queue a game to be host by bots.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeam1",
            "description": "<p>team1 is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidTeam1",
            "description": "<p>team1 is invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeam1Ids",
            "description": "<p>team1Ids is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidTeam1Ids",
            "description": "<p>team1Ids is not an array of integers. Must be of len &gt; 0.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeam2",
            "description": "<p>team2 is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidTeam2",
            "description": "<p>team2 is invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeam2Ids",
            "description": "<p>team2Ids is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidTeam2Ids",
            "description": "<p>team2Ids is not an array of integers. Must be of len &gt; 0.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingName",
            "description": "<p>name is not specified.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidName",
            "description": "<p>name is not valid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingPassword",
            "description": "<p>password is not specified.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidPassword",
            "description": "<p>password is not valid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeamChoosingFirst",
            "description": "<p>teamChoosingFirst is not specified.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidTeamChoosingFirst",
            "description": "<p>teamChoosingFirst is not valid.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "team1",
            "description": "<p>Id of the first team</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer[]",
            "optional": false,
            "field": "team1Ids",
            "description": "<p>SteamID (64bits) of first team players</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "team2",
            "description": "<p>Id of the second team</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer[]",
            "optional": false,
            "field": "team2Ids",
            "description": "<p>SteamID (64bits) of second team  players</p>"
          },
          {
            "group": "Parameter",
            "type": "String[1..]",
            "optional": false,
            "field": "name",
            "description": "<p>Name of the game lobby.</p>"
          },
          {
            "group": "Parameter",
            "type": "String[1..]",
            "optional": false,
            "field": "password",
            "description": "<p>Password for the lobby.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "allowedValues": [
              "1",
              "2"
            ],
            "optional": false,
            "field": "teamChoosingFirst",
            "description": "<p>Team choosing 'side'/'pick order' first.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>Id of the game that will be hosted by bots.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/game.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "get",
    "url": "/api/game/details",
    "title": "GameGetDetails",
    "version": "1.0.1",
    "name": "GameGetDetails",
    "group": "DotaBots",
    "description": "<p>Request game details.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingId",
            "description": "<p>Id is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidId",
            "description": "<p>Id is not an integer.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "NoGameWithId",
            "description": "<p>Id is not present in database.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>Id of the game hosted by bots.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>Id of the game hosted by bots.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of the game lobby.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>Password for the lobby.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "team1",
            "description": "<p>Id of the first team</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "team1Ids",
            "description": "<p>SteamID (64bits) of first team players</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "team2",
            "description": "<p>Id of the second team</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "team2Ids",
            "description": "<p>SteamID (64bits) of second team  players</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "allowedValues": [
              "GameStatus.WAITING_FOR_BOT",
              "GameStatus.CREATION_IN_PROGRESS",
              "GameStatus.WAITING_FOR_PLAYERS",
              "GameStatus.GAME_IN_PROGRESS",
              "GameStatus.COMPLETED",
              "GameStatus.CANCELLED"
            ],
            "optional": false,
            "field": "status",
            "description": "<p>Game status.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "allowedValues": [
              "1",
              "2"
            ],
            "optional": false,
            "field": "teamChoosingFirst",
            "description": "<p>Team choosing 'side'/'pick order' first</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "bot",
            "description": "<p>Steam Bot managing the game (if status not 'GameStatus.WAITING_FOR_BOT')</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "valveId",
            "description": "<p>Game Id in Valve database (if status 'GameStatus.COMPLETED')</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "allowedValues": [
              "1",
              "2"
            ],
            "optional": false,
            "field": "winner",
            "description": "<p>Team winning the game (if status 'GameStatus.COMPLETED')</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/game.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "get",
    "url": "/api/game/details",
    "title": "GameGetDetails",
    "version": "1.0.0",
    "name": "GameGetDetails",
    "group": "DotaBots",
    "description": "<p>Request game details.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingId",
            "description": "<p>Id is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidId",
            "description": "<p>Id is not an integer.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "NoGameWithId",
            "description": "<p>Id is not present in database.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>Id of the game hosted by bots.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>Id of the game hosted by bots.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "team1",
            "description": "<p>Id of the first team</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of the game lobby.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>Password for the lobby.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "team1Ids",
            "description": "<p>SteamID (64bits) of first team players</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "team2",
            "description": "<p>Id of the second team</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "team2Ids",
            "description": "<p>SteamID (64bits) of second team  players</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "allowedValues": [
              "\"GameStatus.WAITING_FOR_BOT\"",
              "\"GameStatus.CREATION_IN_PROGRESS\"",
              "\"GameStatus.WAITING_FOR_PLAYERS\"",
              "\"GameStatus.GAME_IN_PROGRESS\"",
              "\"GameStatus.COMPLETED\"",
              "\"GameStatus.CANCELLED\""
            ],
            "optional": false,
            "field": "status",
            "description": "<p>Game status.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "allowedValues": [
              "1",
              "2"
            ],
            "optional": false,
            "field": "teamChoosingFirst",
            "description": "<p>Team choosing 'side'/'pick order' first</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "valveId",
            "description": "<p>Game Id in Valve database (if status 'GameStatus.COMPLETED')</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "allowedValues": [
              "1",
              "2"
            ],
            "optional": false,
            "field": "winner",
            "description": "<p>Team winning the game (if status 'GameStatus.COMPLETED')</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/_apidoc.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "get",
    "url": "/api/game/list",
    "title": "GameList",
    "version": "1.0.2",
    "name": "GameList",
    "group": "DotaBots",
    "description": "<p>Get the list of multiple hosted games.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidLimit",
            "description": "<p>Limit is not a positive integer in waited range.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidOffset",
            "description": "<p>Offset is not a positive integer in waited range.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidFields",
            "description": "<p>Fields is not an array.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "size": "1-100",
            "optional": true,
            "field": "limit",
            "defaultValue": "10",
            "description": "<p>Optional number of entries to return.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "size": "0-..",
            "optional": true,
            "field": "offset",
            "defaultValue": "0",
            "description": "<p>Optional offset for database fetch.</p>"
          },
          {
            "group": "Parameter",
            "type": "String[]",
            "optional": true,
            "field": "fields",
            "defaultValue": "['name', 'password', 'team1', 'team1Ids', 'team2', 'team2Ids', 'status',\n         'teamChoosingFirst', 'bot', 'valveId', 'winner']",
            "description": "<p>Optional fields to return.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "games",
            "description": "<p>List of the Games ordered by decreasing id, with filters applied.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "games.id",
            "description": "<p>Id of the game hosted by bots.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "games.name",
            "description": "<p>Name of the game lobby.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "games.password",
            "description": "<p>Password for the lobby.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "games.team1",
            "description": "<p>Id of the first team</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "games.team1Ids",
            "description": "<p>SteamID (64bits) of first team players</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "games.team2",
            "description": "<p>Id of the second team</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "games.team2Ids",
            "description": "<p>SteamID (64bits) of second team  players</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "allowedValues": [
              "GameStatus.WAITING_FOR_BOT",
              "GameStatus.CREATION_IN_PROGRESS",
              "GameStatus.WAITING_FOR_PLAYERS",
              "GameStatus.GAME_IN_PROGRESS",
              "GameStatus.COMPLETED",
              "GameStatus.CANCELLED"
            ],
            "optional": false,
            "field": "games.status",
            "description": "<p>Game status.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "allowedValues": [
              "1",
              "2"
            ],
            "optional": false,
            "field": "games.teamChoosingFirst",
            "description": "<p>Team choosing 'side'/'pick order' first</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "games.bot",
            "description": "<p>Steam Bot managing the game (if status not 'GameStatus.WAITING_FOR_BOT')</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "games.valveId",
            "description": "<p>Game Id in Valve database (if status 'GameStatus.COMPLETED')</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "allowedValues": [
              "1",
              "2"
            ],
            "optional": false,
            "field": "games.winner",
            "description": "<p>Team winning the game (if status 'GameStatus.COMPLETED')</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/game.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "post",
    "url": "/api/game/vip/add",
    "title": "GameVIPAdd",
    "version": "1.0.0",
    "name": "GameVIPAdd",
    "group": "DotaBots",
    "description": "<p>Add a new game VIP.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingId",
            "description": "<p>id is not specified.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidId",
            "description": "<p>id is invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "VIPWithIdAlreadyExists",
            "description": "<p>VIP with id is already in database.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingType",
            "description": "<p>type is not specified.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidType",
            "description": "<p>type is not valid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingName",
            "description": "<p>name is not specified.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidName",
            "description": "<p>name is not valid.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>SteamId (64bits) of the vip to add.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "CASTER",
              "ADMIN"
            ],
            "optional": false,
            "field": "type",
            "description": "<p>Type of the vip to add.</p>"
          },
          {
            "group": "Parameter",
            "type": "String[1..]",
            "optional": false,
            "field": "name",
            "description": "<p>Name of the vip to add.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/game.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "get",
    "url": "/api/game/vip/list",
    "title": "GameVIPList",
    "version": "1.0.0",
    "name": "GameVIPList",
    "group": "DotaBots",
    "description": "<p>Get the list of all VIPs</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "vips",
            "description": "<p>List of the VIPs authorized in all games.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "vips.id",
            "description": "<p>Steam Id of the VIP.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "allowedValues": [
              "GameVIPType.CASTER",
              "GameVIPType.ADMIN"
            ],
            "optional": false,
            "field": "vips.type",
            "description": "<p>Type of the VIP.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "vips.name",
            "description": "<p>Name of the VIP.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/game.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "post",
    "url": "/api/game/vip/remove",
    "title": "GameVIPRemove",
    "version": "1.0.0",
    "name": "GameVIPRemove",
    "group": "DotaBots",
    "description": "<p>Remove a game VIP.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingId",
            "description": "<p>id is not specified.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidId",
            "description": "<p>id is invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "VIPDoesNotExist",
            "description": "<p>VIP with id does not exist in the database.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>SteamId of the vip to remove.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/game.py",
    "groupTitle": "DotaBots"
  },
  {
    "type": "get",
    "url": "/api/obs/scene/list",
    "title": "OBSSceneList",
    "version": "1.0.4",
    "name": "OBSSceneList",
    "group": "StreamSystem",
    "description": "<p>List the available scenes in OBS.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InternalOBSError",
            "description": "<p>Error communicating to OBS.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "scenes",
            "description": "<p>All available scenes with their name as Strings.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/obs/scene/update",
    "title": "OBSSceneUpdate",
    "version": "1.0.4",
    "name": "OBSSceneUpdate",
    "group": "StreamSystem",
    "description": "<p>Change the OBS current scene to a new one</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>Restricted API_KEY necessary to call the endpoint.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyMissing",
            "description": "<p>Missing API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ApiKeyInvalid",
            "description": "<p>Invalid API_KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InternalOBSError",
            "description": "<p>Error communicating to OBS.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingScene",
            "description": "<p>The scene with the specified name doesn't exist.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "scene",
            "description": "<p>Name of the scene to change to.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "get",
    "url": "/api/user/details",
    "title": "UserGetDetails",
    "version": "1.0.4",
    "name": "UserGetDetails",
    "group": "User",
    "description": "<p>This method returns multiple information about a user that logged at least one time.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "id",
            "description": "<p>SteamID (64bits) of the user to request.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Errors": [
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingIdParameter",
            "description": "<p>Id is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidIdParameter",
            "description": "<p>Invalid id value (not an int).</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "UserNotFound",
            "description": "<p>There is no user in the database with this id.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "id",
            "description": "<p>SteamID (64bits).</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/user.py",
    "groupTitle": "User"
  }
] });
