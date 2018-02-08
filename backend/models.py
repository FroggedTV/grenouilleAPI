import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ScalarListType

db = SQLAlchemy()

class UserRefreshToken(db.Model):
    """The only valid refresh token for this user..

    Attributes:
        id: Steam unique identifier 64bits.
        token: String of the valid token
    """
    __tablename__ = 'user_refresh_token'

    id = db.Column(db.BigInteger(), primary_key=True)
    refresh_token = db.Column(db.String(), primary_key=True)

    @staticmethod
    def get(id):
        """Returns the token of a specific user.

        Args:
            id: Steam unique identifier.
        Returns:
            UserRefreshToken of the target user or None if no refresh token existing.
        """
        return UserRefreshToken.query.filter_by(id=id).one_or_none()

    @staticmethod
    def upsert(id, token):
        """Upsert the current refresh token valid for a user.

        Args:
            id: Steam unique identifier of the user.
            token: Refresh JWT of the user.
        Returns:
            UserRefreshToken of the target user, with the token updated.
        """
        user_refresh_token = UserRefreshToken.get(id)
        if user_refresh_token is None:
            user_refresh_token = UserRefreshToken()
            user_refresh_token.id = id
            db.session.add(user_refresh_token)
        user_refresh_token.refresh_token = token
        db.session.commit()

        return user_refresh_token

    @staticmethod
    def revoke(id):
        """Revoke the token of a specified user when logout.

        Args:
            id: Steam unique identifier of the user.
        """
        UserRefreshToken.query.filter_by(id=id).delete()
        db.session.commit()

class User(db.Model):
    """A user representation in the database.

    Attributes:
        id: Steam unique identifier 64bits.
        nickname: user nickname.
        avatar: user avatar as a 64bits string.
        verified_nickname: boolean if the user is validated (nickname locked).
    """
    __tablename__ = 'user'

    id = db.Column(db.BigInteger(), primary_key=True)
    nickname = db.Column(db.String(), nullable=False)
    nickname_verified = db.Column(db.Boolean(), nullable=False)
    avatar = db.Column(db.String(), nullable=False)

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
        self.type = GameVIPType[type]
        self.name = name

    @staticmethod
    def get_all_vips():
        """Get the list of all VIPs authorized to get inside all lobbies."""
        vips = []
        for vip in db.session().query(GameVIP).all():
            vips.append({'id': vip.id,
                         'type': str(vip.type),
                         'name': vip.name})
        return vips
