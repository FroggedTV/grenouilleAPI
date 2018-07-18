***

### Endpoints access

Some endpoints are free to use but most of them are protected in 2 possible ways, either with a user login or an API-key. Such endpoints require a full auth process to be accessed. All API calls are limited to 200 per minutes per ip.
* If the application is a web based application where the user needs to login, this application will use the `RefreshTokenGetWithSteam` endpoint to get a `JWT`.
* In other cases, the application with use an application key to get a `JWT`, using `RefreshTokenGetWithKey` endpoint.

Refresh tokens are long lived (60 days) and must be saved in a secured place. They give access to `AuthTokenGet` endpoint, generating a Auth token. This token is short lived (1 hour) and contains user scopes (endpoint restrictions).

### Parameter format

A typical GET curl command to access an endpoint is:

```
curl -X GET --header "<HEADER>" https://grenouilleapi.the-cluster.org/api/<ENDPOINT>?data=<DATA>
```

* `<HEADER>` use the format `Authorization: Bearer <TOKEN>` with a valid `JWT` token.
* `<ENDPOINT>` is a valid endpoint path.
* `<DATA>` is a JSON object representing parameters as a urlencoded string.


A typical POST curl command to access an endpoint is:

```
curl -X POST --header "<HEADER>" -d "<JSON_PAYLOAD>" https://grenouilleapi.the-cluster.org/api/<ENDPOINT>
```

* `<HEADER>` use the format `Authorization: Bearer <TOKEN>` with a valid `JWT` token.
* `<ENDPOINT>` is a valid endpoint path.
* `<JSON_PAYLOAD>` is the JSON payload of data posted.

### Return format

Every endpoint returns a normalized JSON answer with the following format:

```
{
  "error": "<>", 
  "payload": {}, 
  "success": "<>"
}
```

where `success` contains either 
* `yes` if the endpoint behavior is normal, then `payload` contains the object answer from the API.
* `no` if the endpoint behavior as an error, then `error` contains the string error code.

***

## Authentication

Authentication module, either with Steam for a user, or with an api key for other applications.

## DotaBots

Bots used to host in-house leagues.

## User 

User management endpoints.

## Community

Community endpoints for news, calendar, comments.

## StreamSystem

Endpoints used for the automatic streaming system, managing VODs and the forever running OBS.
