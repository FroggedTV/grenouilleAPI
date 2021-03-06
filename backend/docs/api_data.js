define({ "api": [
  {
    "type": "post",
    "url": "/api/auth/key/add",
    "title": "APIKeyAdd",
    "version": "1.1.0",
    "name": "APIKeyAdd",
    "group": "Authentication",
    "description": "<p>Add a new APIKey into the system.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterMissing",
            "description": "<p>Key is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterInvalid",
            "description": "<p>Key is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyAlreadyExists",
            "description": "<p>Key is already in the system.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DescriptionParameterMissing",
            "description": "<p>Description is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DescriptionParameterInvalid",
            "description": "<p>Description is not valid String.</p>"
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
            "field": "key",
            "description": "<p>APIKey to add to the system.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "description",
            "description": "<p>Key description for information.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "post",
    "url": "/api/auth/key/description/update",
    "title": "APIKeyDescriptionUpdate",
    "version": "1.1.0",
    "name": "APIKeyDescriptionUpdate",
    "group": "Authentication",
    "description": "<p>Update the description of an APIKey.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterMissing",
            "description": "<p>Key is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterInvalid",
            "description": "<p>Key is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyDoesntExists",
            "description": "<p>There is no such key in the system.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DescriptionParameterMissing",
            "description": "<p>Description is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DescriptionParameterInvalid",
            "description": "<p>Description is not valid String.</p>"
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
            "field": "key",
            "description": "<p>APIKey to update the description.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "description",
            "description": "<p>Key description for information.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/key/list",
    "title": "APIKeyList",
    "version": "1.1.0",
    "name": "APIKeyList",
    "group": "Authentication",
    "description": "<p>List all APIKeys.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "LimitInvalid",
            "description": "<p>Limit is not a positive integer in waited range.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OffsetInvalid",
            "description": "<p>Offset is not a positive integer in waited range.</p>"
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
            "field": "keys",
            "description": "<p>All available scopes.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "keys.hash",
            "description": "<p>Hash of the API_KEY.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "keys.description",
            "description": "<p>API Key description.</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "keys.scopes",
            "description": "<p>List of scopes this KEY has access to.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "post",
    "url": "/api/auth/key/remove",
    "title": "APIKeyRemove",
    "version": "1.1.0",
    "name": "APIKeyRemove",
    "group": "Authentication",
    "description": "<p>Remove an APIKey from the system.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterMissing",
            "description": "<p>Key is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterInvalid",
            "description": "<p>Key is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyDoesntExists",
            "description": "<p>There is no such key in the system.</p>"
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
            "field": "key",
            "description": "<p>APIKey to add to the system.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "post",
    "url": "/api/auth/key/scope/add",
    "title": "APIKeyScopeAdd",
    "version": "1.1.0",
    "name": "APIKeyScopeAdd",
    "group": "Authentication",
    "description": "<p>Add scope access to the APIKey.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterMissing",
            "description": "<p>Key is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterInvalid",
            "description": "<p>Key is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyDoesntExists",
            "description": "<p>There is no such key in the system.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ScopesParameterMissing",
            "description": "<p>Scope is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ScopesParameterInvalid",
            "description": "<p>Scope is not list of valid scope Strings.</p>"
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
            "field": "key",
            "description": "<p>APIKey to add scopes to.</p>"
          },
          {
            "group": "Parameter",
            "type": "String[]",
            "optional": false,
            "field": "scopes",
            "description": "<p>Scopes to add to the key.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "post",
    "url": "/api/auth/key/scope/remove",
    "title": "APIKeyScopeRemove",
    "version": "1.1.0",
    "name": "APIKeyScopeRemove",
    "group": "Authentication",
    "description": "<p>Remove scope access to the APIKey.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterMissing",
            "description": "<p>Key is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyParameterInvalid",
            "description": "<p>Key is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyDoesntExists",
            "description": "<p>There is no such key in the system.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ScopesParameterMissing",
            "description": "<p>Scope is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ScopesParameterInvalid",
            "description": "<p>Scope is not list of valid scope Strings.</p>"
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
            "field": "key",
            "description": "<p>APIKey to remove scopes from.</p>"
          },
          {
            "group": "Parameter",
            "type": "String[]",
            "optional": false,
            "field": "scopes",
            "description": "<p>Scopes to remove from the key.</p>"
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
    "title": "AuthTokenGet",
    "version": "1.1.0",
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
            "field": "token",
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization header not well formated.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "RefreshTokenExpired",
            "description": "<p>Refresh token has expired and client should get a new one.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "RefreshTokenRevoked",
            "description": "<p>Refresh token has has been revoked and client should get a new one.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "RefreshTokenInvalid",
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
    "url": "/api/auth/login/key",
    "title": "RefreshTokenGetWithKey",
    "version": "1.1.0",
    "name": "RefreshTokenGetWithKey",
    "group": "Authentication",
    "description": "<p>Get a refresh token using a API Key.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "API_KEY",
            "description": "<p>API_KEY necessary to call the endpoint.</p>"
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
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>Refresh token long lived to request access data.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/login/steam",
    "title": "RefreshTokenGetSteam",
    "version": "1.1.0",
    "name": "RefreshTokenGetWithSteam",
    "group": "Authentication",
    "description": "<p>First endpoint to call in the auth process with user. Calling it redirects to the steam login page. After login, the user is redirected to a callback url with the refresh token as a parameter. The URL is defined in the backend config. Frontend must be able to manage the token incoming as a parameter.</p>",
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/scope/list",
    "title": "ScopeList",
    "version": "1.1.0",
    "name": "ScopeList",
    "group": "Authentication",
    "description": "<p>List all available scopes for APIKey and users.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
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
            "field": "scopes",
            "description": "<p>All available scopes.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "post",
    "url": "/api/auth/user/scope/add",
    "title": "UserScopeAdd",
    "version": "1.1.0",
    "name": "UserScopeAdd",
    "group": "Authentication",
    "description": "<p>Add scope access to a user.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "IdParameterMissing",
            "description": "<p>id is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "IdParameterInvalid",
            "description": "<p>id is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "UserWithIdDoesntExists",
            "description": "<p>There is no user with such id in the system.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ScopesParameterMissing",
            "description": "<p>Scope is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ScopesParameterInvalid",
            "description": "<p>Scope is not list of valid scope Strings.</p>"
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
            "field": "id",
            "description": "<p>User id to add scopes to.</p>"
          },
          {
            "group": "Parameter",
            "type": "String[]",
            "optional": false,
            "field": "scopes",
            "description": "<p>Scopes to add to the user.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "get",
    "url": "/api/auth/user/scope/list",
    "title": "UserScopeList",
    "version": "1.1.0",
    "name": "UserScopeList",
    "group": "Authentication",
    "description": "<p>List all users with their scopes.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "LimitInvalid",
            "description": "<p>Limit is not a positive integer in waited range.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OffsetInvalid",
            "description": "<p>Offset is not a positive integer in waited range.</p>"
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
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "total",
            "description": "<p>Total number of users.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "users",
            "description": "<p>All available users.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "users.id",
            "description": "<p>Id of the user.</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "users.scopes",
            "description": "<p>List of scopes this user has access to.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "post",
    "url": "/api/auth/user/scope/remove",
    "title": "UserScopeRemove",
    "version": "1.1.0",
    "name": "UserScopeRemove",
    "group": "Authentication",
    "description": "<p>Remove scope access from a user.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "IdParameterMissing",
            "description": "<p>id is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "IdParameterInvalid",
            "description": "<p>id is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "UserWithIdDoesntExists",
            "description": "<p>There is no user with such id in the system.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ScopesParameterMissing",
            "description": "<p>Scope is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ScopesParameterInvalid",
            "description": "<p>Scope is not list of valid scope Strings.</p>"
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
            "field": "id",
            "description": "<p>User id to remove scopes from.</p>"
          },
          {
            "group": "Parameter",
            "type": "String[]",
            "optional": false,
            "field": "scopes",
            "description": "<p>Scopes to remove from the user.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/auth.py",
    "groupTitle": "Authentication"
  },
  {
    "type": "",
    "url": "{post",
    "title": "/api/calendar/generate CalendarGenerate",
    "version": "1.1.0",
    "name": "CalendarGenerate",
    "group": "Calendar",
    "description": "<p>Generate the calendar backgrounds.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "GoogleCalendarError",
            "description": "<p>Impossible to get data events from GoogleCalendar.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/calendar.py",
    "groupTitle": "Calendar"
  },
  {
    "type": "get",
    "url": "/api/stats/img/generate",
    "title": "StatsCSVGenerateIMG",
    "version": "1.1.0",
    "name": "StatsCSVGenerateIMG",
    "group": "Stats",
    "description": "<p>Start the generation of CSV image.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyInvalid",
            "description": "<p>key is not a valid string.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OpenDotaNotReady",
            "description": "<p>Data is not ready on OpenDota.</p>"
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
            "field": "key",
            "description": "<p>CSV key to generate.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "payload",
            "description": "<p>Optional payload to refine the generation with.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stats.py",
    "groupTitle": "Stats"
  },
  {
    "type": "get",
    "url": "/api/stats/csv/get",
    "title": "StatsCSVGet",
    "version": "1.1.0",
    "name": "StatsCSVGet",
    "group": "Stats",
    "description": "<p>Get CSV saved for stats.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyInvalid",
            "description": "<p>key is not a valid string.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyDataDoesntExist",
            "description": "<p>key has no data associated.</p>"
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
            "field": "key",
            "description": "<p>CSV key to get.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "csv",
            "description": "<p>CSVData associated to the key.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stats.py",
    "groupTitle": "Stats"
  },
  {
    "type": "get",
    "url": "/api/stats/csv/update",
    "title": "StatsCSVUpdate",
    "version": "1.1.0",
    "name": "StatsCSVUpdate",
    "group": "Stats",
    "description": "<p>Update CSV saved for stats.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "KeyInvalid",
            "description": "<p>key is not a valid string.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ValueInvalid",
            "description": "<p>value is not a valid string.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ValueCSVInvalid",
            "description": "<p>value CSV is not a valid same length column csv.</p>"
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
            "field": "key",
            "description": "<p>CSV key to get.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "value",
            "description": "<p>CSV data.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stats.py",
    "groupTitle": "Stats"
  },
  {
    "type": "get",
    "url": "/api/stats/scene/get",
    "title": "StatsSceneGet",
    "version": "1.1.0",
    "name": "StatsSceneGet",
    "group": "Stats",
    "description": "<p>Get the stat image.</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "img",
            "description": "<p>Image to use in the stat scene.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "last_modified",
            "description": "<p>Last time the file was modified.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "continue",
            "description": "<p>Should the stat scene user continue.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stats.py",
    "groupTitle": "Stats"
  },
  {
    "type": "get",
    "url": "/api/stats/scene/status/get",
    "title": "StatsSceneStatusGet",
    "version": "1.1.0",
    "name": "StatsSceneStatusGet",
    "group": "Stats",
    "description": "<p>Get the status of the stat scene.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "activated",
            "description": "<p>Boolean to show if the stat scene is activated or disabled.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stats.py",
    "groupTitle": "Stats"
  },
  {
    "type": "get",
    "url": "/api/stats/scene/status/update",
    "title": "StatsSceneStatusUpdate",
    "version": "1.1.0",
    "name": "StatsSceneStatusUpdate",
    "group": "Stats",
    "description": "<p>Update the status of the stat scene.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ActivatedInvalid",
            "description": "<p>activated is not a valid boolean.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": false,
            "field": "activated",
            "description": "<p>New value of the stat scene status.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "activated",
            "description": "<p>Boolean to show if the stat scene is activated or disabled.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stats.py",
    "groupTitle": "Stats"
  },
  {
    "type": "get",
    "url": "/api/stats/scene/update",
    "title": "StatsSceneUpdate",
    "version": "1.1.0",
    "name": "StatsSceneUpdate",
    "group": "Stats",
    "description": "<p>Update the stat scene.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ImgInvalid",
            "description": "<p>img is not a valid string.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ImgNoFile",
            "description": "<p>img is not a valid file image.</p>"
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
            "field": "img",
            "description": "<p>New scene.</p>"
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
            "field": "img",
            "description": "<p>Image to show appended with a cache bang.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "last_modified",
            "description": "<p>Last time the file was modified.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stats.py",
    "groupTitle": "Stats"
  },
  {
    "type": "get",
    "url": "/api/obs/playlist/get",
    "title": "OBSPlaylistGet",
    "version": "1.1.0",
    "name": "OBSPlaylistGet",
    "group": "StreamSystem",
    "description": "<p>Get OBS playlist content for replay.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
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
            "field": "files",
            "description": "<p>List of file paths inside the playlist.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/obs/playlist/update",
    "title": "OBSPlaylistUpdate",
    "version": "1.1.0",
    "name": "OBSPlaylistUpdate",
    "group": "StreamSystem",
    "description": "<p>Set OBS playlist content for replay.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
            "description": "<p>Error communicating to OBS.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FilesParameterMissing",
            "description": "<p>files is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FilesParameterInvalid",
            "description": "<p>files is not list of valid file paths.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AtLeastOneFileDoesntExist",
            "description": "<p>files is not list of valid file paths.</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String[]",
            "optional": false,
            "field": "files",
            "description": "<p>List of file paths to build the playlist from.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/obs/record/start",
    "title": "OBSRecordStart",
    "version": "1.1.0",
    "name": "OBSRecordStart",
    "group": "StreamSystem",
    "description": "<p>Start the recording by OBS.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
            "description": "<p>Error communicating to OBS.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSAlreadyRecording",
            "description": "<p>OBS is already recording.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/obs/record/stop",
    "title": "OBSRecordStop",
    "version": "1.1.0",
    "name": "OBSRecordStop",
    "group": "StreamSystem",
    "description": "<p>Stop the recording by OBS.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
            "description": "<p>Error communicating to OBS.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSNotRecording",
            "description": "<p>OBS is not currently recording.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/obs/rtmp/restart",
    "title": "OBSRestartRTMP",
    "version": "1.1.0",
    "name": "OBSRestartRTMP",
    "group": "StreamSystem",
    "description": "<p>Force the restart of the RTMP docker image.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DockerClientError",
            "description": "<p>Impossible to manipulate docker with client.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "get",
    "url": "/api/obs/scene/list",
    "title": "OBSSceneList",
    "version": "1.1.0",
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
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
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
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "active_scene",
            "description": "<p>Active scene.</p>"
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
    "version": "1.1.0",
    "name": "OBSSceneUpdate",
    "group": "StreamSystem",
    "description": "<p>Change the OBS active scene to a new one.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
            "description": "<p>Error communicating to OBS.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "SceneParameterMissing",
            "description": "<p>Scene is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "SceneParameterInvalid",
            "description": "<p>Scene is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "SceneDoesNotExist",
            "description": "<p>Specified scene does not exist in OBS.</p>"
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
    "url": "/api/obs/status",
    "title": "OBSStatus",
    "version": "1.1.0",
    "name": "OBSStatus",
    "group": "StreamSystem",
    "description": "<p>Get OBS streaming and recording status.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
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
            "type": "Boolean",
            "optional": false,
            "field": "recording",
            "description": "<p>Status of the OBS record.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "streaming",
            "description": "<p>Status of the OBS stream.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/obs/stream/start",
    "title": "OBSStreamStart",
    "version": "1.1.0",
    "name": "OBSStreamStart",
    "group": "StreamSystem",
    "description": "<p>Start the streaming by OBS.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
            "description": "<p>Error communicating to OBS.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSAlreadyStreaming",
            "description": "<p>OBS already streaming to endpoint.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/obs/stream/stop",
    "title": "OBSStreamStop",
    "version": "1.1.0",
    "name": "OBSStreamStop",
    "group": "StreamSystem",
    "description": "<p>Stop the streaming by OBS.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSInternalError",
            "description": "<p>Error communicating to OBS.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "OBSNotStreaming",
            "description": "<p>OBS is not currently streaming.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/vod/dir/create",
    "title": "VODDirCreate",
    "version": "1.1.0",
    "name": "VODDirCreate",
    "group": "StreamSystem",
    "description": "<p>Create a directory for VOD.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FileSystemError",
            "description": "<p>Internal error manipulating the filesystem.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DirParameterMissing",
            "description": "<p>dir is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DirParameterInvalid",
            "description": "<p>dir is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DirAlreadyExists",
            "description": "<p>There is no VOD file or directory with the specified filename.</p>"
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
            "field": "dir",
            "description": "<p>Path of the dir to create, without any &quot;.&quot; character. &quot;/&quot; are accepted for sub directories.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "get",
    "url": "/api/vod/disk_usage",
    "title": "VODDiskUsage",
    "version": "1.1.0",
    "name": "VODDiskUsage",
    "group": "StreamSystem",
    "description": "<p>Get the disk usage of all the VOD directory.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FileSystemError",
            "description": "<p>Internal error manipulating the filesystem.</p>"
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
            "field": "size",
            "description": "<p>Size of the root directory in octets.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/vod/file/delete",
    "title": "VODFileDelete",
    "version": "1.1.0",
    "name": "VODFileDelete",
    "group": "StreamSystem",
    "description": "<p>Delete a VOD file or directory.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FileSystemError",
            "description": "<p>Internal error manipulating the filesystem.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FilenameParameterMissing",
            "description": "<p>Filename is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FilenameParameterInvalid",
            "description": "<p>Filename is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "VODFileDoesntExist",
            "description": "<p>There is no VOD file or directory with the specified filename.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "VODDirectoryNotEmpty",
            "description": "<p>Impossible to remove a directory not empty.</p>"
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
            "field": "filename",
            "description": "<p>Path of the file to delete (equal to what vod_file_list returns).</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "get",
    "url": "/api/vod/file/list",
    "title": "VODFileList",
    "version": "1.1.0",
    "name": "VODFileList",
    "group": "StreamSystem",
    "description": "<p>List all VOD files, omitting VOD_PATH root.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FileSystemError",
            "description": "<p>Internal error manipulating the filesystem.</p>"
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
            "field": "entry",
            "description": "<p>List of all VOD directories and files.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "entry.name",
            "description": "<p>Name of the entry.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "allowedValues": [
              "dir",
              "file"
            ],
            "optional": false,
            "field": "entry.type",
            "description": "<p>Type of the entry.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "entry.size",
            "description": "<p>Size of the entry if type is 'file', in octets.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "post",
    "url": "/api/vod/file/move",
    "title": "VODFileMove",
    "version": "1.1.0",
    "name": "VODFileMove",
    "group": "StreamSystem",
    "description": "<p>Move a VOD file.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessRefused",
            "description": "<p>Client has no scope access to target endpoint.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "FileSystemError",
            "description": "<p>Internal error manipulating the filesystem.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "SourceParameterMissing",
            "description": "<p>Source is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "SourceParameterInvalid",
            "description": "<p>Source is not valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "SourceFileDoesntExist",
            "description": "<p>There is no VOD file with the specified source path.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DestinationParameterMissing",
            "description": "<p>Destination is not present in the parameters.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DestinationParameterInvalid",
            "description": "<p>Destination is not a valid String.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DestinationFileAlreadyExist",
            "description": "<p>There is already a file with such path.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "DestinationRootDirectoryMissing",
            "description": "<p>Destination path has no root directory created yet.</p>"
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
            "field": "source",
            "description": "<p>Path of the file to move (equal to what vod_file_list returns).</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "destination",
            "description": "<p>Path where to move the file.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/stream_system.py",
    "groupTitle": "StreamSystem"
  },
  {
    "type": "get",
    "url": "/api/user/me/details",
    "title": "UserMeDetails",
    "version": "1.1.0",
    "name": "UserMeDetails",
    "group": "User",
    "description": "<p>Get detailed information of myself, scopes, id...</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>'Bearer &lt;Auth_Token&gt;'</p>"
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
            "field": "AuthorizationHeaderInvalid",
            "description": "<p>Authorization Header is Invalid.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenExpired",
            "description": "<p>Token has expired, must be refreshed by client.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "AuthTokenInvalid",
            "description": "<p>Token is invalid, decode is impossible.</p>"
          },
          {
            "group": "Errors",
            "type": "String",
            "optional": false,
            "field": "ClientAccessImpossible",
            "description": "<p>This type of client can't access target endpoint.</p>"
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
            "field": "steam_id",
            "description": "<p>Steam ID of the user.</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "scopes",
            "description": "<p>List of scopes this user has access to.</p>"
          }
        ]
      }
    },
    "filename": "backend/routes/user.py",
    "groupTitle": "User"
  }
] });
