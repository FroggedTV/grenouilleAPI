define({ "api": [
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
  }
] });
