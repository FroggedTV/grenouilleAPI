import logging
import pickle
import random
from gevent import Greenlet, sleep
from threading import Lock

from app import create_app
from dota_bot import DotaBot
from models import db, DynamicConfiguration, Game, GameStatus, GameVIP
from helpers import divide_vip_list_per_type

# Log
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s', level=logging.INFO)


class Credential:
    """A Steam account credentials.

    Attributes:
        login: Steam user login.
        password: Steam user password.
    """

    def __init__(self, login, password):
        """Create a user credentials.

        Args:
            login: user login.
            password: user password.
        """
        self.login = login
        self.password = password


class WorkerManager(Greenlet):
    """Master class starting Dota bots to process jobs.

    The manager contains a initial pool of Steam Credentials.
    It is a thread pooling jobs from the database, starting new Dota bots when a new job is available.
    After a job process, the Dota bot informs that the credentials are available again.

    Attributes:
        app: The flask application the manager is linked to, containing configuration objects and database access.
        working_bots: A dictionary of all currently working Dota bots, indexed by bot login.
    """

    def __init__(self):
        """Initialize the worker manager thread."""
        Greenlet.__init__(self)

        # Initialize
        self.app = create_app()
        self.working_bots = {}
        self.credentials = []
        self.mutex = Lock()

        # Parse credentials from config
        bot_credentials_string = self.app.config['STEAM_BOTS']
        bot_credentials = bot_credentials_string.split('@')

        i = 0
        while i < len(bot_credentials):
            login = bot_credentials[i]
            password = bot_credentials[i+1]
            self.credentials.append(Credential(login, password))
            i = i + 2

    def _run(self):
        """Start the main loop of the thread, creating Dota bots to process available jobs."""
        while True:
            with self.app.app_context():
                admins, casters = divide_vip_list_per_type(GameVIP.get_all_vips())
                bot_pause = DynamicConfiguration.get('bot_pause', 'False')
                for game in db.session().query(Game)\
                                        .filter(Game.status==GameStatus.WAITING_FOR_BOT)\
                                        .order_by(Game.id).all():
                    if len(self.credentials) == 0 or bot_pause == 'True':
                        continue

                    # Start a Dota bot to process the game
                    self.mutex.acquire()
                    credential = self.credentials.pop(random.randint(0, len(self.credentials) - 1))
                    g = DotaBot(self, credential, admins, casters, game.id, game.name, game.password,
                                game.team1, game.team2, game.team1_ids, game.team2_ids, game.team_choosing_first)
                    self.working_bots[credential.login] = g
                    game.status = GameStatus.CREATION_IN_PROGRESS
                    game.bot = credential.login
                    db.session().commit()
                    g.start()
                    self.mutex.release()
            sleep(60)

    def bot_end(self, credential):
        """Signal that a bot has finished it work and the credential is free to use again.

        Args:
            credential: `Credential` of the bot.
        """
        self.mutex.acquire()
        self.working_bots.pop(credential.login)
        self.credentials.append(credential)
        self.mutex.release()


# Start a Manager if this file is the main script.
if __name__ == '__main__':
    g = WorkerManager()
    g.start()
    g.join()
