define({ "api": [
  {
    "type": "get",
    "url": "/api/auth/token_test",
    "title": "1.2 - Dummy display of a Refresh Token",
    "name": "DisplayToken",
    "group": "Authentication",
    "description": "<p>Test function used to display the token generated after the steam login. This must not be used in production, but only as a token displayer in dev.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>The refresh token to display.</p>"
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
            "field": "token",
            "description": "<p>The refresh token displayed.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/token",
    "title": "2 - Get a Auth Token from a Refresh Token",
    "name": "GetAuthToken",
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
    "version": "0.0.0",
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/login",
    "title": "1.1 - Get a Refresh Token with Steam Login",
    "name": "GetRefreshToken",
    "group": "Authentication",
    "description": "<p>Calling this endpoint redirects to the steam login page. After login, the user is redirected to a callback url with the refresh token as a parameter. The URL is defined in the backend config.</p>",
    "version": "0.0.0",
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "post",
    "url": "/api/game/vip/add",
    "title": "AddGameVIP",
    "name": "AddGameVIP",
    "group": "Game",
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
              "\"CASTER\"",
              "\"ADMIN\""
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
    "version": "0.0.0",
    "filename": "backend/routes/game.py",
    "groupTitle": "Game"
  },
  {
    "type": "post",
    "url": "/api/game/create",
    "title": "CreateGame",
    "name": "CreateGame",
    "group": "Game",
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
    "version": "0.0.0",
    "filename": "backend/routes/game.py",
    "groupTitle": "Game"
  },
  {
    "type": "get",
    "url": "/api/game/details",
    "title": "GetGameDetails",
    "name": "GetGameDetails",
    "group": "Game",
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
    "version": "0.0.0",
    "filename": "backend/routes/game.py",
    "groupTitle": "Game"
  },
  {
    "type": "get",
    "url": "/api/game/vip/list",
    "title": "ListGameVIPs",
    "name": "ListGameVIPs",
    "group": "Game",
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
              "\"GameVIPType.CASTER\"",
              "\"GameVIPType.ADMIN\""
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
    "version": "0.0.0",
    "filename": "backend/routes/game.py",
    "groupTitle": "Game"
  },
  {
    "type": "post",
    "url": "/api/game/vip/remove",
    "title": "RemoveGameVIP",
    "name": "RemoveGameVIP",
    "group": "Game",
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
    "version": "0.0.0",
    "filename": "backend/routes/game.py",
    "groupTitle": "Game"
  },
  {
    "type": "get",
    "url": "/api/user/details",
    "title": "GetUserDetails",
    "name": "GetUserDetails",
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
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "id",
            "description": "<p>SteamID (64bits).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "nickname",
            "description": "<p>Username.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "nickname_verified",
            "description": "<p>True if user nickname is locked because verified.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "avatar",
            "description": "<p>User avatar as a 64bits string.</p>"
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
    "version": "0.0.0",
    "filename": "backend/routes/user.py",
    "groupTitle": "User"
  }
] });
