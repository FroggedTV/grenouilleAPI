# Global

### Endpoints access
Endpoints are protected with 2 possible ways, specified in endpoint headers. API calls are limited to 200 per minutes per ip.

First you can use an APIKey if the <API_KEY> header is present. Otherwise, if you have a logged user, you can use a auth token in the <Authorization> header. In this case, the user needs to have the appropriate user rights to use the endpoint. 

### Parameter format

A typical curl command to access an endpoint is:

```
curl -X <COMMAND> --header "API_KEY: <KEY>" -d "<JSON_PAYLOAD>" https://grenouilleapi.the-cluster.org/api/<ENDPOINT>
```

* `<COMMAND>` is `GET` or `POST`.
* `<KEY>` is a valid API key if necessary.
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
User authentication module. User logs with steam, and is redirected to the website with a refresh token valid for 60 days. The refresh token is then used to get a auth token, valid for 1 hour. The auth token is the base of User-based endpoint access.

## DotaBots

Bots used to host inhouse leagues.

## User 

User management endpoints.

## Community

Community endpoints for news, calendar, comments.

## StreamSystem

Endpoints used for the automatic streaming system, managing VODs and the forever running OBS.
