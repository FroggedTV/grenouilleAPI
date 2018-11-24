import enum

from database import db

class Scope(enum.Enum):
    API_KEY_SCOPE = 'api_key_scope'           # Management of the API_KEYs
    USER_SCOPE = 'user_scope'                 # Management of the user rights
    OBS_CONTROL = 'obs_control'               # Send commands to OBS
    VOD_MANAGE = 'vod_manage'                 # Manage VODs on disk
    VOD_DELETE = 'vod_delete'                 # Delete VODs on disk
    STATS_MANAGE = 'stats_manage'             # Work on stats
    STATS_MANAGE_SCENE = 'stats_manage_scene' # Modify the stat displayed on scene
    CALENDAR = 'calendar'                     # Update and see the calendar

class UserScope(db.Model):
    """All scopes available for a user.

    Args:
        id: User id.
        channel: channel the scope is used on.
        scope: scope.
    """
    __tablename__ = 'user_scope'

    id = db.Column(db.BigInteger(), db.ForeignKey('user.id'), primary_key=True)
    channel = db.Column(db.String(), primary_key=True)
    scope = db.Column(db.String(), primary_key=True)

    def __init__(self, id, channel, scope):
        self.id = id
        self.channel = channel
        self.scope = scope

    @staticmethod
    def upsert(id, channel, scope):
        """Add a scope to a user on a specific channel.

        Args:
            id: user id.
            channel: channel the scope is used on.
            scope: scope to add.
        """

        user_scope = db.session().query(UserScope).filter(UserScope.id==id, UserScope.channel==channel, UserScope.scope==scope).one_or_none()
        if user_scope is None:
            user_scope = UserScope(id, channel, scope)
            db.session.add(user_scope)
            db.session.commit()

        return user_scope

    @staticmethod
    def remove(id, channel, scope):
        """Remove a scope for a user.

        Args:
            id: user id.
            channel: channel the scope is used on.
            scope: scope to remove.
        Returns:
            True if the scope was removed, False otherwise.
        """
        user_scope = db.session().query(UserScope).filter(UserScope.id==id, UserScope.channel==channel, UserScope.scope==scope).one_or_none()
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
        scopes = {}
        for scope in db.session().query(UserScope).filter(UserScope.id==id).all():
            if scope.channel not in scopes:
                scopes[scope.channel] = []
            scopes[scope.channel].append(scope.scope)

        return scopes

    @staticmethod
    def get_channel_specific(id, channel):
        """Get all scopes of a single user on a specific channel.

        Args:
            id: user id
            channel: channel to list scope from
        Returns:
            List of scopes
        """
        scopes = []
        for scope in db.session().query(UserScope).filter(UserScope.id==id, UserScope.channel==channel).all():
            scopes.append(scope.scope)

        return scopes

class APIKeyScope(db.Model):
    """All scopes available for an APIKey.

    Args:
        key_hash: User id.
        channel: channel the scope is used on.
        scope: scope.
    """
    __tablename__ = 'api_key_scope'

    key_hash = db.Column(db.String(), db.ForeignKey('api_key.key_hash'), primary_key=True)
    channel = db.Column(db.String(), primary_key=True)
    scope = db.Column(db.String(), primary_key=True)

    def __init__(self, key_hash, channel, scope):
        self.key_hash = key_hash
        self.channel = channel
        self.scope = scope

    @staticmethod
    def upsert(key_hash, channel, scope):
        """Add a scope to a APIKey.

        Args:
            key_hash: APIKey hash.
            channel: channel the scope is used on.
            scope: scope to add.
        """

        api_scope = db.session().query(APIKeyScope).filter(APIKeyScope.key_hash==key_hash, APIKeyScope.channel==channel, APIKeyScope.scope==scope).one_or_none()
        if api_scope is None:
            api_scope = APIKeyScope(key_hash, channel, scope)
            db.session.add(api_scope)
            db.session.commit()

        return api_scope

    @staticmethod
    def remove(key_hash, channel, scope):
        """Remove a scope for a APIKey.

        Args:
            key_hash: APIKey hash.
            channel: channel the scope is used on.
            scope: scope to remove.
        Returns:
            True if the scope was removed, False otherwise.
        """
        api_scope = db.session().query(APIKeyScope).filter(APIKeyScope.key_hash==key_hash, APIKeyScope.channel==channel, APIKeyScope.scope==scope).one_or_none()
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
        scopes = {}
        for scope in db.session().query(APIKeyScope).filter(APIKeyScope.key_hash==key_hash).all():
            if scope.channel not in scopes:
                scopes[scope.channel] = []
            scopes[scope.channel].append(scope.scope)

        return scopes
