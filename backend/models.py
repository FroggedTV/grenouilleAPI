import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ScalarListType

db = SQLAlchemy()

#########################
# User, APIKeys, Scopes #
#########################

class User(db.Model):
    """A user representation in the database.

    Attributes:
        id: Steam unique identifier 64bits.
        refresh_token: current refresh_token valid for this user
    """
    __tablename__ = 'user'

    id = db.Column(db.BigInteger(), primary_key=True)
    refresh_token = db.Column(db.String(), nullable=True)

    def __init__(self, id):
        """Instantiate a new user with default values.

        Args:
            id: Steam unique identifier 64bits.
        """
        self.id = id

    @staticmethod
    def get(id):
        """Returns the user defined by a unique identifier.

        Args:
            id: Steam unique identifier.
        Returns:
            User object with the provided identifier or None if there is no
            User with this identifier.
        """
        return User.query.filter_by(id=id).one_or_none()

class APIKey(db.Model):
    """An API Key used in the system

    Attributes:
        key_hash: sha1 of a valid API_KEY.
        description: description of the API key usage.
        refresh_token: current refresh_token valid for this API_KEY
    """
    __tablename__ = 'api_key'

    key_hash = db.Column(db.String(), primary_key=True)
    description = db.Column(db.String(), nullable=True)
    refresh_token = db.Column(db.String(), nullable=True)

    def __init__(self, key_hash, description=None):
        self.key_hash = key_hash
        self.description = description

    @staticmethod
    def get(key_hash):
        """Returns the APIKey data if found.

        Args:
            key_hash: sha1 hash of the key to find data about.
        Returns:
            APIKey object if it exists, none otherwise.
        """
        return APIKey.query.filter_by(key_hash=key_hash).one_or_none()

class Scope(enum.Enum):
    API_KEY_SCOPE = 'api_key_scope'           # Management of the API_KEYs
    USER_SCOPE = 'user_scope'                 # Management of the user rights
    OBS_CONTROL = 'obs_control'               # Send commands to OBS
    VOD_MANAGE = 'vod_manage'                 # Manage VODs on disk
    VOD_DELETE = 'vod_delete'                 # Delete VODs on disk
    STATS_MANAGE = 'stats_manage'             # Work on stats
    STATS_MANAGE_SCENE = 'stats_manage_scene' # Modify the stat displayed on scene

class UserScope(db.Model):
    """All scopes available for a user.

    Args:
        id: User id.
        scope: scope.
    """
    __tablename__ = 'user_scope'

    id = db.Column(db.BigInteger(), db.ForeignKey('user.id'), primary_key=True)
    scope = db.Column(db.String(), primary_key=True)

    def __init__(self, id, scope):
        self.id = id
        self.scope = scope

    @staticmethod
    def upsert(id, scope):
        """Add a scope to a user.

        Args:
            id: user id.
            scope: scope to add.
        """

        user_scope = db.session().query(UserScope).filter(UserScope.id==id, UserScope.scope==scope).one_or_none()
        if user_scope is None:
            user_scope = UserScope(id, scope)
            db.session.add(user_scope)
            db.session.commit()

        return user_scope

    @staticmethod
    def remove(id, scope):
        """Remove a scope for a user.

        Args:
            id: user id.
            scope: scope to remove.
        Returns:
            True if the scope was removed, False otherwise.
        """
        user_scope = db.session().query(UserScope).filter(UserScope.id==id, UserScope.scope==scope).one_or_none()
        if user_scope is None:
            return False
        else:
            db.session.delete(user_scope)
            db.session.commit()
            return True

    @staticmethod
    def get_all(id):
        """Get all scopes of a single user.

        Args:
            id: user id
        Returns:
            List of scopes
        """
        scopes = []
        for scope in db.session().query(UserScope).filter(UserScope.id==id).all():
            scopes.append(scope.scope)

        return scopes

class APIKeyScope(db.Model):
    """All scopes available for an APIKey.

    Args:
        key_hash: User id.
        scope: scope.
    """
    __tablename__ = 'api_key_scope'

    key_hash = db.Column(db.String(), db.ForeignKey('api_key.key_hash'), primary_key=True)
    scope = db.Column(db.String(), primary_key=True)

    def __init__(self, key_hash, scope):
        self.key_hash = key_hash
        self.scope = scope

    @staticmethod
    def upsert(key_hash, scope):
        """Add a scope to a APIKey.

        Args:
            key_hash: APIKey hash.
            scope: scope to add.
        """

        api_scope = db.session().query(APIKeyScope).filter(APIKeyScope.key_hash==key_hash, APIKeyScope.scope==scope).one_or_none()
        if api_scope is None:
            api_scope = APIKeyScope(key_hash, scope)
            db.session.add(api_scope)
            db.session.commit()

        return api_scope

    @staticmethod
    def remove(key_hash, scope):
        """Remove a scope for a APIKey.

        Args:
            key_hash: APIKey hash.
            scope: scope to remove.
        Returns:
            True if the scope was removed, False otherwise.
        """
        api_scope = db.session().query(APIKeyScope).filter(APIKeyScope.key_hash==key_hash, APIKeyScope.scope==scope).one_or_none()
        if api_scope is None:
            return False
        else:
            db.session.delete(api_scope)
            db.session.commit()
            return True

    @staticmethod
    def get_all(key_hash):
        """Get all scopes of a single APIKey.

        Args:
            key_hash: APIKey hash.
        Returns:
            List of scopes
        """
        scopes = []
        for scope in db.session().query(APIKeyScope).filter(APIKeyScope.key_hash==key_hash).all():
            scopes.append(scope.scope)

        return scopes

###################
# Games, GameVIPs #
###################

class GameStatus(enum.Enum):
    WAITING_FOR_BOT = 'Waiting for a bot to start and pick the game.'
    CREATION_IN_PROGRESS = 'Bot is creating the game inside the client.'
    WAITING_FOR_PLAYERS = 'Game is created, waiting for players to join.'
    GAME_IN_PROGRESS = 'Game is in progress.'
    COMPLETED = 'Game completed.'
    CANCELLED = 'Game cancelled.'

class Game(db.Model):
    """A game managed by bots."""
    __tablename__= 'game'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    team1 = db.Column(db.Integer(), nullable=False)
    team2 = db.Column(db.Integer(), nullable=False)
    team1_ids = db.Column(ScalarListType(int), nullable=False)
    team2_ids = db.Column(ScalarListType(int), nullable=False)

    status = db.Column(db.Enum(GameStatus), nullable=False)
    team_choosing_first = db.Column(db.Integer(), nullable=False)

    bot = db.Column(db.String(), nullable=True)
    valve_id = db.Column(db.BigInteger(), nullable=True)
    winner = db.Column(db.Integer(), nullable=True)

    def __init__(self, name, password, team1, team2, team1_ids, team2_ids, team_choosing_first=1):
        self.name = name
        self.password = password
        self.team1 = team1
        self.team2 = team2
        self.team1_ids = team1_ids
        self.team2_ids = team2_ids
        self.status = GameStatus.WAITING_FOR_BOT
        self.team_choosing_first = team_choosing_first
        self.bot = None
        self.valve_id = None
        self.winner = None

class GameVIPType(enum.Enum):
    CASTER = 'CASTER'
    ADMIN = 'ADMIN'

class GameVIP(db.Model):
    """A game VIP who can enter every game."""
    __tablename__ = 'game_vip'

    id = db.Column(db.BigInteger(), primary_key=True)
    type = db.Column(db.Enum(GameVIPType), nullable=False)
    name = db.Column(db.String(), nullable=False)

    def __init__(self, id, type, name):
        self.id = id
        self.type = type
        self.name = name

    @staticmethod
    def get_all_vips():
        """Get the list of all VIPs authorized to get inside all lobbies."""
        vips = []
        for vip in db.session().query(GameVIP).order_by(GameVIP.id).all():
            vips.append({'id': vip.id,
                         'type': str(vip.type),
                         'name': vip.name})
        return vips

    @staticmethod
    def upsert(id, type, name):
        vip = db.session().query(GameVIP).filter(GameVIP.id==id).one_or_none()
        if vip is None:
            vip = GameVIP(id, type, name)
            db.session.add(vip)
        else:
            vip.type = type
            vip.name = name
        db.session.commit()

###########
# Various #
###########

class DynamicConfiguration(db.Model):
    """Dynamic configuration used by multiple elements, modified using the API."""
    __tablename__ = 'dynamic_configuration'

    key = db.Column(db.String(), primary_key=True)
    value = db.Column(db.String(), nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @staticmethod
    def get(key, default_value):
        """Get the value of a configuration key.

        Attributes:
            key: key of the configuration.
            default_value: value if not present in database.
        Returns:
            The value associated with the key.
        """
        dc = db.session().query(DynamicConfiguration).filter(DynamicConfiguration.key==key).one_or_none()
        if dc is None:
            return default_value
        else:
            return dc.value

    @staticmethod
    def update(key, value):
        dc = db.session().query(DynamicConfiguration).filter(DynamicConfiguration.key==key).one_or_none()
        if dc is None:
            dc = DynamicConfiguration(key, value)
            db.session().add(dc)
        dc.value = value
        db.session().commit()
        return dc

class CSVData(db.Model):
    """CSV Holders"""
    __tablename__= 'csv_data'

    key = db.Column(db.String(), primary_key=True)
    value = db.Column(db.Text(), nullable=False)

    def __init__(self, key):
        self.key = key

    @staticmethod
    def upsert(key, value):
        data = db.session.query(CSVData).filter(CSVData.key==key).one_or_none()
        if data is None:
            data = CSVData(key)
            db.session.add(data)
        data.value = value
        db.session.commit()

class DotaHero(db.Model):
    """Dota heroes"""
    __tablename__= 'dota_heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    short_name = db.Column(db.Text(), nullable=False)
    localized_name = db.Column(db.Text(), nullable=False)

    def __init__(self, id, name, short_name, localized_name):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.localized_name = localized_name

    @staticmethod
    def upsert(id, name, short_name, localized_name):
        hero = db.session.query(DotaHero).filter(DotaHero.id==id).one_or_none()
        if hero is None:
            hero = DotaHero(id, name, short_name, localized_name)
            db.session.add(hero)
        hero.id = id
        hero.name = name
        hero.short_name = short_name
        hero.localized_name = localized_name
        db.session.commit()

class DotaItem(db.Model):
    """Dota items"""
    __tablename__= 'dota_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    short_name = db.Column(db.Text(), nullable=False)
    localized_name = db.Column(db.Text(), nullable=False)

    def __init__(self, id, name, short_name, localized_name):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.localized_name = localized_name

    @staticmethod
    def upsert(id, name, short_name, localized_name):
        item = db.session.query(DotaItem).filter(DotaItem.id==id).one_or_none()
        if item is None:
            item = DotaItem(id, name, short_name, localized_name)
            db.session.add(item)
        item.id = id
        item.name = name
        item.short_name = short_name
        item.localized_name = localized_name
        db.session.commit()
