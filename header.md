## Endpoints access
Endpoints are protected with 2 possible ways, specified in endpoint headers. API calls are limited to 50 per minutes per ip.

First you can use an APIKey if the <API_KEY> header is present. If you have a logged user, you can use a auth token in the <Authorization> header. In this case, the user needs to have the appropriate user rights to use the endpoint. 

## Authentication
User authentication module. User logs with steam, and is redirected to the website with a refresh token valid for 60 days. The refresh token is then used to get a auth token, valid for 1 hour. The token is used to access multiple endpoints.

## DotaBots

Bots used to host inhouse leagues.

## User 

User management endpoints.

## Community

Community endpoints for news, calendar, comments.

## StreamSystem

Endpoints used for the automatic streaming system, managing VODs and the forever running OBS.
