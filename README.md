# GrenouilleAPI

## TODO List

### API

Endpoints:
- [X] Change documentation function names
- [X] Fix versioning in documentation
- [ ] Add a `ListGames(limit, offset)`, ordered by `id desc`
- [ ] Add `limit` and `offset` to `ListGameVIPs(limit, offset)`

### BOT

Features:
- [X] VIPs enter lobby, CASTER can enter casting slots, ADMIN stay spectator
- [X] CASTERs can authorize a co-caster to enter the lobby, with !cocast <SteamID>
- [X] ADMINs can authorize standins to enter the lobby, with !standin <SteanID> <Team>
- [X] Add a !destroy command so ADMINs can hard cancel a lobby
- [X] Test host inside S1 Ticket
- [X] Add bot login to Game entry inside db
- [X] Test if bots status is inside db

- [ ] Retry if someone does not connect. 3 retries, 5min between each.
- [ ] !ready to start game, and not when players are all in position
- [ ] Test host inside S2 ticket
- [ ] Bot leaves chats that are not lobby chat

Code design:
- [X] Bot secure cancel, destroy Greenlet and every sleeping events.
- [ ] Refactor main loop (player waiting, side/order, waiting again, retry, game waiting, result)
- [ ] Function documentations

## General Documentation

The grenouilleAPI repository is composed of 3 main parts: the **Database**, the **Web API**, the **DotaBOT** section.
 
The **Database** part is a generic storage for the API and also connected to the DotaBOT. 
It can take different form: a sqlite file storage for development, or a shared mysql/postgres/maria/..., or the docker image prepared with a postgres database.

### Web API - `backend/app.py`

The **Web API** is a Flask application hosted in a Python Tornado web server, listening to HTTP requests. 
Endpoints are secured with API_KEY defined in the configuration file.

The **Game** section is dedicated to hosting Dota games for the French leagues, managed by automated bots.
The **Authentication** section is dedicated to login users using Steam login, generating JWT for other requests (not ready to use yet).
The **User** section is dedicated to user logged inside the database (not ready to use yet).

### Dota BOT - `backend/bot_app.py`

The **DotaBOT** is a Python3 Greenlet, listening to the database for games to hosts for the French leagues.
The master manager spawns 1 slave greenlet for each game, simulating a Dota client using `ValvePython/dota2` library.

## Technical Documentation

The **Web API** documentation for endpoints is generated with the command `make refresh-docs` in the `backend/docs` folder.
This is a simple web page to open in a browser stored at `backend/docs/index.html`. 
If you host the API (dev or prod), the doc will be available at `//docs/index.html`.

### Development Environment

Install system dependencies for dev with:
```
sudo apt install make python python3-pip libpq-dev libffi-dev
sudo pip3 install --upgrade pip
sudo pip3 install virtualenv
```

Install virtual environment in a `.venv` directory with `make dev-install`. 
Run the API code in dev environment with `make dev-run` and the BOT code with `make dev-botrun`. 
Clean development files (virtual environment) with `make dev-clean`.

### Configuration

Flask production and development app use a setting file `backend/cfg/settings.cfg`.
You have to create it to match your target system.
A setting file example is available at `backend/settings-example.cfg`.

If you use docker to run postgres (which is the case in production), you have to setup the environment variables in `docker/grenouilleapi_postgres/conf.env`.
A environment file example is available at `docker/grenouilleapi_postgres/conf.example.env`

### Database

#### SQLite development

Development run with `make dev-run` with no modification to the configuration file uses a SQLite file saved in `backend/cfg/sqlite.db`

#### Postgres manual setup

You can use any Postgres database as long as you use the good connection url in `backend/cfg/settings.cfg`.

Commands to apply to setup the database
```
psql -c "create user grenouilleapi;"
psql -c "alter user grenouilleapi with superuser;"
psql -c "alter user grenouilleapi with password 'password';"
psql -c "create database grenouilleapi;
```

#### Postgres docker Run

Production uses a Docker Postgres image with a persistent volume saving data into `/home/docker/grenouilleapi_postgres/`.
The same database is usable in development on your machine. Use `make db-docker-start` and `make db-docker-stop` to manage it.

#### Common commands

Once `settings.cfg` file is configured for your database setup, you can apply migration commands to the database.

Apply all migrations to the database with `make db-upgrade` or `make db-docker-upgrade` depending if your database is isolated inside a docker or not.

Backtrack the latest migration on the database with `make db-downgrade` or `make db-docker-downgrade` depending if your database is isolated inside a docker or not.

Generate a new migration file into `backend/migrations/versions` by comparing `backend/models.py` with the running database (upgrade will be applied before the compare) with `make db-migrate`. Use a dev database to generate this migration.

### Production Environment

Production run inside docker images. A postgres image hosts the database, and 2 debian images with tornado/python and dota lib hosts the API and the DotaBot.

Start everything with `make prod-start` and stop everything with `make prod-stop`.

NOTE: You can even use these commands in development because docker ensure isolation.
However, the docker image is built after each code modification, so it's not efficient.

