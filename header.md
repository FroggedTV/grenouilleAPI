# Global

### Endpoints access

Endpoints are protected in 2 possible ways, specified in endpoint headers. API calls are limited to 200 per minutes per ip.
* If the `API_KEY` header is present, you can use the endpoint with such a key. Keys will (TODO) be secured using a `scope`.
* If the `Authorization` header is present, you can use the endpoint as a logged user. You need to follow the authorization process to get a `Refresh` token then a `Auth` token. Endpoints are restricted using `UserRights`.      

### Parameter format

A typical curl command to access an endpoint is:

```
curl -X <COMMAND> --header "<HEADER>" -d "<JSON_PAYLOAD>" https://grenouilleapi.the-cluster.org/api/<ENDPOINT>
```

* `<COMMAND>` is `GET` or `POST`.
* `<HEADER>` is either `API_KEY: <KEY>` with a valid key or `Authorization: Bearer <TOKEN>` for a user accessed endpoint.
* `<ENDPOINT>` is a valid endpoint path.
* `<JSON_PAYLOAD>` is the JSON payload in both `GET` and `POST` cases.

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

# Modules

## Authentication
User authentication module. User logs with Steam, and is redirected to the website with a refresh token valid for 60 days (as a parameter in the URL). The `Refresh` token is then used to get a `Auth` token, valid for 1 hour.

## DotaBots

Bots used to host in-house leagues.

## User 

User management endpoints.

## Community

Community endpoints for news, calendar, comments.

## StreamSystem

Endpoints used for the automatic streaming system, managing VODs and the forever running OBS.
