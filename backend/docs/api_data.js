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
    "type": "get",
    "url": "/api/game/details",
    "title": "GameDetails",
    "name": "GameDetails",
    "group": "Game",
    "description": "<p>Request game details.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API-KEY",
            "description": "<p>Restricted API-KEY necessary to call the endpoint.</p>"
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
            "field": "KeyError",
            "description": "<p>Missing or invalid API-KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingHostIdParameter",
            "description": "<p>hostId is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidHostIdParameter",
            "description": "<p>hostId is not a valid id or not present.</p>"
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
            "field": "hostId",
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
            "type": "String",
            "optional": false,
            "field": "hostId",
            "description": "<p>Id of the game hosted by bots.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "team1",
            "description": "<p>Name of the first team</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "team1Ids",
            "description": "<p>SteamID (64bits) of first team players, separated by ','</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "team2",
            "description": "<p>Name of the second team</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "team2Ids",
            "description": "<p>SteamID (64bits) of second team  players, separated by ','</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "spectatorIds",
            "description": "<p>SteamID (64bits) of spectator players, separated by ',' (Optional)</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "status",
            "description": "<p>Game status. Possible values are 'waiting bot', 'creation in progress', 'waiting for players', 'game in progress', 'completed', 'canceled'.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "valveId",
            "description": "<p>Game Id in Valve database.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "coinTossWinner",
            "description": "<p>Winner of the coin toss: 'team1' or 'team2'.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "team1Choice",
            "description": "<p>Choice after the coin toss for team1: 'fp', 'sp', 'radiant' or 'dire'</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "team2Choice",
            "description": "<p>Choice after the coin toss for team2: 'fp', 'sp', 'radiant' or 'dire'</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "winner",
            "description": "<p>Winner of the game: 'team1' or 'team2'.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "team1NoJoin",
            "description": "<p>Number of players who didn't join the lobby from team1.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "team2NoJoin",
            "description": "<p>Number of players who didn't join the lobby from team2.</p>"
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
    "url": "/api/game/host",
    "title": "HostGame",
    "name": "HostGame",
    "group": "Game",
    "description": "<p>Queue a game to host by bots.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API-KEY",
            "description": "<p>Restricted API-KEY necessary to call the endpoint.</p>"
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
            "field": "KeyError",
            "description": "<p>Missing or invalid API-KEY header.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeam1Parameter",
            "description": "<p>team1 is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeam1IdsParameter",
            "description": "<p>team1Ids is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidTeam1IdsParameter",
            "description": "<p>team1Ids is not a list of steamIds.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeam2Parameter",
            "description": "<p>team2 is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "MissingTeam2IdsParameter",
            "description": "<p>team2Ids is not present.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "InvalidTeam2IdsParameter",
            "description": "<p>team2Ids is not a list of steamIds.</p>"
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
            "field": "team1",
            "description": "<p>Name of the first team</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "team1Ids",
            "description": "<p>SteamID (64bits) of first team players, separated by ','</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "team2",
            "description": "<p>Name of the second team</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "team2Ids",
            "description": "<p>SteamID (64bits) of second team  players, separated by ','</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "spectatorIds",
            "description": "<p>SteamID (64bits) of spectator players, separated by ',' (Optional)</p>"
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
            "field": "hostId",
            "description": "<p>Id of the game hosted by bots for further requests.</p>"
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
