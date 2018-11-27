import logging
import json
import time
import os
from datetime import datetime
import hashlib

from flask_script import Manager

from app import create_app
from database import db
from models.Stream import Stream
from models.User import User, APIKey
from models.UserScope import Scope, UserScope, APIKeyScope
from models.DotaBots import Game, GameStatus, GameVIP, GameVIPType
from models.DotaData import DotaHero, DotaItem, DotaProPlayer, DotaProTeam
from helpers.obs import send_command_to_obs

app = create_app()
manager = Manager(app)

###########
# Scripts #
###########

@manager.command
def hello_world():
    """Simple script example."""
    print('Hello World')

@manager.option('--key', dest='key', default=None)
@manager.option('--description', dest='description', default=None)
def add_api_key(key, description):
    """Add a new API Key to the system.

    Args:
        key: key value string to add.
        description: key description as a reminder.
    """
    if key is None:
        print('No API key specified')
        return
    if description is None:
        print('No description specified')
        return

    salt = app.config['API_KEY_SALT']
    hash_object = hashlib.sha1((key + salt).encode('utf-8'))
    hash_key = hash_object.hexdigest()
    api_key = db.session().query(APIKey).filter(APIKey.key_hash == hash_key).one_or_none()

    if api_key is not None:
        print('Key already in the system')
    else:
        key = APIKey(hash_key, description)
        db.session().add(key)
        db.session().commit()
        print('Key added')

@manager.option('--key', dest='key', default=None)
@manager.option('--channel', dest='channel', default=None)
@manager.option('--scope', dest='scope', default=None)
def add_scope_api_key(key, channel, scope):
    """Add a scope to target APIKey

    Args:
        key: key value.
        channel: channel to add the scope to.
        scope: scope to add.
    """
    if key is None:
        print('No API key specified')
        return
    if channel is None:
        print('No channel specified')
        return
    if scope is None:
        print('No scope specified')
        return
    if scope not in [x.value for x in list(Scope)]:
        print('Invalid scope')
        return

    salt = app.config['API_KEY_SALT']
    hash_object = hashlib.sha1((key + salt).encode('utf-8'))
    hash_key = hash_object.hexdigest()
    api_key = db.session().query(APIKey).filter(APIKey.key_hash == hash_key).one_or_none()

    if api_key is None:
        print('Key not present!')
    else:
        APIKeyScope.upsert(api_key.key_hash, channel, scope)
        print('Scope added')

@manager.option('--id', dest='id', default=None)
@manager.option('--channel', dest='channel', default=None)
@manager.option('--scope', dest='scope', default=None)
@manager.option('--force', dest='force', default=False)
def add_scope_user(id, channel, scope, force):
    """Add a scope to a steam ID.

    Args:
        id: user steam ID value.
        channel: channel to add the scope to.
        scope: scope to add.
        force: force adding user to database.
    """
    if id is None:
        print('No user steamId')
        return
    if channel is None:
        print('No channel specified')
        return
    if scope is None:
        print('No scope specified')
        return
    if scope not in [x.value for x in list(Scope)]:
        print('Invalid scope')
        return
    user = db.session().query(User).filter(User.id == id).one_or_none()

    if user is None:
        if force is False:
            print('User not present!')
            return
        else:
            user = User(id)
            db.session.add(user)
            db.session.commit()

    UserScope.upsert(user.id, channel, scope)
    print('Scope added')

@manager.command
def clean_rogue_scopes():
    """Clean rogue scopes from database."""
    all_scopes = [x.value for x in list(Scope)]
    for user_scope in db.session.query(UserScope).all():
        if user_scope.scope not in all_scopes:
            db.session.delete(user_scope)
    for key_scope in db.session.query(APIKeyScope).all():
        if key_scope.scope not in all_scopes:
            db.session.delete(key_scope)
    db.session.commit()

@manager.command
def init_database():
    """Initialize database with dota value."""
    # Insert Streams
    Stream.upsert(id='froggedtv', name='FroggedTV', hostname='127.0.0.1', port=4444, google_calendar_id='qnv4k3c3upl94sj41pui158k3c@group.calendar.google.com')
    Stream.upsert(id='artifact_fr', name='Artifact_FR', hostname='127.0.0.1', port=4445, google_calendar_id='j2e6a18f0bqm8h21vko77vbag0@group.calendar.google.com')

    # Insert Heroes
    hero_json_path = os.path.join(os.path.dirname(__file__), 'ressources', 'json', 'dota_heroes.json')
    if os.path.isfile(hero_json_path):
        with open(hero_json_path, 'r') as hero_json_file:
            hero_json = json.loads(hero_json_file.read())
        for hero in hero_json['heroes']:
            DotaHero.upsert(hero['id'], hero['name'], hero['short_name'], hero['localized_name'])

    # Insert Items
    item_json_path = os.path.join(os.path.dirname(__file__), 'ressources', 'json', 'dota_items.json')
    if os.path.isfile(item_json_path):
        with open(item_json_path, 'r') as item_json_file:
            item_json = json.loads(item_json_file.read())
        for item in item_json['items']:
            DotaItem.upsert(item['id'], item['name'], item['short_name'], item['localized_name'])

    # Insert Pro Players
    players_json_path = os.path.join(os.path.dirname(__file__), 'ressources', 'json', 'dota_pro_players.json')
    if os.path.isfile(players_json_path):
        with open(players_json_path, 'r') as players_json_file:
            players_json = json.loads(players_json_file.read())
        for player in players_json['players']:
            DotaProPlayer.upsert(player['account_id'], player['name'], player['nickname'], player['team_id'])

    # Insert Pro Teams
    teams_json_path = os.path.join(os.path.dirname(__file__), 'ressources', 'json', 'dota_pro_teams.json')
    if os.path.isfile(teams_json_path):
        with open(teams_json_path, 'r') as teams_json_file:
            teams_json = json.loads(teams_json_file.read())
        for team in teams_json['teams']:
            DotaProTeam.upsert(team['id'], team['name'])

@manager.command
def restart_stream_if_live():
    """Command to restart the streaming by disconnecting the obs live, then reconnecting it."""
    try:
        ret = send_command_to_obs('GetStreamingStatus', {})
        if not ret['streaming']:
            return

        send_command_to_obs('StopStreaming', {})
        time.sleep(5)
        send_command_to_obs('StartStreaming', {})
    except Exception as e:
        logging.exception(e)

#######################
# Setup Manage Script #
#######################
if __name__ == '__main__':
    manager.run()
