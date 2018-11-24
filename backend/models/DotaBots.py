import enum
from sqlalchemy_utils import ScalarListType

from database import db

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
