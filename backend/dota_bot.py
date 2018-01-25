import logging
from gevent import Greenlet, sleep

from steam import SteamClient, SteamID
import dota2
from dota2.enums import DOTA_GC_TEAM, EMatchOutcome

from app import create_app
from models import db, Game, GameStatus


class DotaBot(Greenlet):
    """A worker thread, connecting to steam to process a unique job.

    Attributes:
        worker_manager: `WorkerManager` this bot is linked to.
        credential: `Credential` used to connect to steam.
    """

    def __init__(self, worker_manager, credential, id, name, password, team1, team2, team1_ids, team2_ids,
                 team_choosing_first):
        """Initialize the Dota bot thread for a unique job process.

        Args:
            worker_manager: `DazzarWorkerManager` this bot is linked to.
            credential: `Credential` used to connect to steam.
        """
        Greenlet.__init__(self)

        # High Level properties
        self.credential = credential
        self.worker_manager = worker_manager
        self.app = self.worker_manager.app

        self.client = SteamClient()
        self.dota = dota2.Dota2Client(self.client)

        # Game settings
        self.id = id
        self.name = name
        self.password = password
        self.team1 = team1
        self.team2 = team2
        self.team1_ids = team1_ids
        self.team2_ids = team2_ids
        self.team_choosing_first = team_choosing_first

        # State machine variables
        self.job_started = False
        self.job_finished = False
        self.lobby_status = {}
        """
        self.game_creation_call = False

        self.match = None
        self.players = None

        self.game_status = None
        self.lobby_channel_id = None
        self.invite_timer = None
        self.missing_players = None
        self.missing_players_count = None
        self.wrong_team_players = None
        self.wrong_team_players_count = None
        """

        # Prepare all event handlers
        # - Steam client events
        # - Dota client events
        # - Bot events
        self.client.on('connected', self.steam_connected)
        self.client.on('logged_on', self.steam_logged)
        self.client.on('disconnected', self.steam_disconnected)

        self.dota.on('ready', self.dota_ready)
        self.dota.on('notready', self.closed_dota)

        self.dota.on(dota2.features.Lobby.EVENT_LOBBY_NEW, self.game_hosted)
        self.dota.on(dota2.features.Lobby.EVENT_LOBBY_CHANGED, self.game_update)

        """
        self.dota.on(dota2.features.Chat.EVENT_CHANNEL_JOIN, self.channel_join)
        self.dota.on(dota2.features.Chat.EVENT_CHANNEL_MESSAGE, self.channel_message)
        """


    def _run(self):
        """Start the main loop of the thread, connecting to Steam, waiting for the job to finish to close the bot."""
        self.print_info('Connecting to Steam...')
        self.client.connect(retry=None)  # Try connecting with infinite retries

        while not self.job_finished:
            sleep(10)

        self.client.disconnect()
        self.worker_manager.bot_end(self.credential)

    # Helpers

    def print_info(self, trace):
        """Wrapper of `logging.info` with bot name prefix.

        Args:
            trace: String to output as INFO.
        """
        logging.info('%s: %s', self.credential.login, trace)

    def print_error(self, trace):
        """Wrapper of `logging.error` with bot name prefix.

        Args:
            trace: String to output as ERROR.
        """
        logging.error("%s: %s", self.credential.login, trace)

    # Callback of Steam and Dota clients

    def steam_connected(self):
        """Callback fired when the bot is connected to Steam, login user."""
        self.print_info('Connected to Steam.')
        self.client.login(self.credential.login, self.credential.password)

    def steam_logged(self):
        """Callback fired when the bot is logged into Steam, starting Dota."""
        self.print_info('Logged to Steam.')
        self.dota.launch()

    def steam_disconnected(self):
        """Callback fired when the bot is disconnected from Steam"""
        self.print_info('Disconnected from Steam.')

    def dota_ready(self):
        """Callback fired when the Dota application is ready, resume the job processing."""
        self.print_info('Dota application is ready.')
        sleep(10) # Safety to leave already existing lobby if bot is lost in the matrix
        self.host_game()

    def closed_dota(self):
        """Callback fired when the Dota application is closed."""
        self.print_info('Dota application is closed.')

    # Messaging events
    """
    def end_job_processing(self):
        self.print_info('Job ended.')
        self.job = None
        self.job_finished = True

    def channel_join(self, channel_info):
        if channel_info.channel_type != dota2.enums.DOTAChatChannelType_t.DOTAChannelType_Lobby:
            self.dota.leave_channel(channel_info.channel_id)
        else:
            if self.game_status is not None:
                if channel_info.channel_name == 'Lobby_{0}'.format(self.game_status.lobby_id):
                    self.lobby_channel_id = channel_info.channel_id

    def channel_message(self, message):
        pass
    """

    # Hosting events
    def host_game(self):
        """Start the processing of the job with the appropriate handler."""
        # Safety check
        if not self.job_started :
            self.job_started = True
        else:
            return
        self.print_info('Hosting game {0} with password {1}'.format(self.name, self.password))
        self.dota.create_practice_lobby(password=self.password)

    def game_hosted(self, message):
        """Callback fired when the Dota bot enters a lobby."""
        if not self.job_started:
            self.dota.leave_practice_lobby()
        else:
            self.lobby_status = message
            with self.app.app_context():
                game = db.session().query(Game).filter(Game.id==self.id).one_or_none()
                if game is not None:
                    game.status = GameStatus.WAITING_FOR_PLAYERS
                    db.session().commit()
            self.initialize_lobby()
            # P1: Wait for people to join for 25 minutes, P2 if slots are filled (X=min remaining)
            # P2: Give 1min for each teams to pick sides/picks
            # P3: Give min(1, 30-X-2) min for teams to get into slots, starts when both teams ready, or time passed
            # P4: wait for game to finish
            # P5: report results
            sleep(60)
            self.dota.leave_practice_lobby()
            self.job_finished = True
            """
            start = self.manage_player_waiting()

            if not start:
                self.dota.send_message(self.lobby_channel_id, 'Annulation de la partie.')
                self.process_game_dodge()
            else:
                self.dota.send_message(self.lobby_channel_id, 'Tous les joueurs sont présents.')
                self.start_game()

                # Waiting PostGame = 3 or UI = 0 (means no loading)
                while self.game_status.state != 0 and self.game_status.state != 3:
                    sleep(5)

                if self.game_status.state == 0:
                    self.process_game_dodge()
                elif self.game_status.state == 3:
                    self.process_endgame_results()

            if self.lobby_channel_id is not None:
                self.dota.leave_channel(self.lobby_channel_id)
                self.lobby_channel_id = None

            self.dota.leave_practice_lobby()
            self.end_job_processing()
            """

    def game_update(self, message):
        """Callback fired when the game lobby change, update local information."""
        self.lobby_status = message

    def initialize_lobby(self):
        """Setup the game lobby with the good options, and change status in database."""
        self.print_info('Game %s created, setup.' % self.name)

        #self.dota.join_lobby_channel()
        self.dota.join_practice_lobby_team()
        options = {
            'game_name': self.name,
            'pass_key': self.password,
            'game_mode': dota2.enums.DOTA_GameMode.DOTA_GAMEMODE_CM,
            'server_region': int(dota2.enums.EServerRegion.Europe),
            'fill_with_bots': False,
            'allow_spectating': True,
            'allow_cheats': False,
            'allchat': False,
            'dota_tv_delay': 2,
            'pause_setting': 1
        }
        self.dota.config_practice_lobby(options=options)
        """
        with self.app.app_context():
            match = Match.query.filter_by(id=self.job.match_id).first()
            match.status = constants.MATCH_STATUS_WAITING_FOR_PLAYERS
            db.session.commit()
            """
    #
    # def manage_player_waiting(self):
    #     """Wait for players to join the lobby with actions depending on player actions.
    #
    #     Returns:
    #         A boolean that indicates if the game should be started after the player waiting process.
    #     """
    #     self.invite_timer = timedelta(minutes=5)
    #     self.compute_player_status()
    #     refresh_rate = 10
    #
    #     while self.invite_timer != timedelta(0):
    #         for player in self.missing_players:
    #             self.dota.invite_to_lobby(player)
    #         sleep(refresh_rate)
    #         self.compute_player_status()
    #
    #         if len(self.missing_players) == 0 and len(self.wrong_team_players) == 0:
    #             return True
    #         else:
    #             if self.invite_timer.seconds != 0 and self.invite_timer.seconds % 60 in [0, 30]:
    #                 minutes = self.invite_timer.seconds // 60
    #                 seconds = self.invite_timer.seconds - 60*minutes
    #                 self.dota.send_message(self.lobby_channel_id,
    #                                        '{:01d}:{:02d} avant annulation, {} absent(s), {} mal placé(s).'.format(
    #                                            minutes, seconds, self.missing_players_count, self.wrong_team_players_count))
    #             self.invite_timer = self.invite_timer - timedelta(seconds=refresh_rate)
    #     return False
    #
    # def compute_player_status(self):
    #     """Helpers to manage player status from protobuff message.
    #
    #     Invite all missing players to come to the lobby.
    #     Kick all players not supposed to be inside a lobby.
    #     Kick from slots all players not in the good slot.
    #     """
    #     self.missing_players = []
    #     self.missing_players_count = 0
    #     self.wrong_team_players = []
    #     self.wrong_team_players_count = 0
    #
    #     for player_id, player in self.players.items():
    #         self.missing_players_count +=1
    #         self.missing_players.append(player_id)
    #
    #     for message_player in self.game_status.members:
    #         if message_player.id == self.dota.steam_id:
    #             continue
    #         if message_player.id in self.missing_players:
    #             self.missing_players_count -= 1
    #             self.missing_players.remove(message_player.id)
    #             good_slot = message_player.slot == self.players[message_player.id].team_slot
    #             good_team = (message_player.team == DOTA_GC_TEAM.GOOD_GUYS and
    #                          self.players[message_player.id].is_radiant) or \
    #                         (message_player.team == DOTA_GC_TEAM.BAD_GUYS and
    #                          not self.players[message_player.id].is_radiant)
    #             if not (good_team and good_slot):
    #                 self.wrong_team_players.append(message_player.id)
    #                 self.wrong_team_players_count += 1
    #                 if message_player.team != DOTA_GC_TEAM.PLAYER_POOL:
    #                     self.dota.practice_lobby_kick_from_team(SteamID(message_player.id).as_32)
    #         else:
    #             # Say: Kick joueur non authorisé message_player.name
    #             self.dota.practice_lobby_kick(SteamID(message_player.id).as_32)
    #
    # def process_game_dodge(self):
    #     """Punish players stopping game start."""
    #     self.print_info('Game %s cancelled because of dodge.' % self.job.match_id)
    #
    #     # Say: Partie annulée - punish
    #     with self.app.app_context():
    #         match = Match.query.filter_by(id=self.job.match_id).first()
    #         match.status = constants.MATCH_STATUS_CANCELLED
    #         self.compute_player_status()
    #         for player in PlayerInMatch.query. \
    #                 options(joinedload_all('player')). \
    #                 filter(PlayerInMatch.match_id == self.job.match_id). \
    #                 all():
    #             if player.player.current_match == self.job.match_id:
    #                 player.player.current_match = None
    #
    #             # Update Scoreboard
    #             if player.player_id in self.missing_players or player.player_id in self.wrong_team_players:
    #                 score = Scoreboard.query.filter_by(ladder_name=match.section, user_id=player.player_id).first()
    #                 if score is None:
    #                     score = Scoreboard(user=player.player, ladder_name=match.section)
    #                     db.session.add(score)
    #                 player.is_dodge = True
    #                 score.points -= 2
    #                 score.dodge += 1
    #         db.session.commit()
    #
    # def start_game(self):
    #     """Start the Dota game and update status in database."""
    #     self.print_info('Launching game %s' % self.job.match_id)
    #
    #     self.dota.launch_practice_lobby()
    #     sleep(10)
    #     with self.app.app_context():
    #         match = Match.query.filter_by(id=self.job.match_id).first()
    #         match.status = constants.MATCH_STATUS_IN_PROGRESS
    #         if self.game_status.connect is not None and self.game_status.connect[0:1] == '=[':
    #             match.server = self.game_status.connect[2:-1]
    #         elif self.game_status.server_id is not None:
    #             match.server = self.game_status.server_id
    #         db.session.commit()
    #     sleep(10)
    #
    # def process_endgame_results(self):
    #     """After a game, process lobby results into database."""
    #     self.print_info('Game %s over.' % self.job.match_id)
    #
    #     with self.app.app_context():
    #         match = Match.query.filter_by(id=self.job.match_id).first()
    #         match.status = constants.MATCH_STATUS_ENDED
    #         match.server = None
    #         if self.game_status.match_outcome == 2:
    #             match.radiant_win = True
    #         elif self.game_status.match_outcome == 3:
    #             match.radiant_win = False
    #         else:
    #             match.radiant_win = None
    #
    #         self.players = {}
    #         for player in PlayerInMatch.query. \
    #                 options(joinedload_all('player')). \
    #                 filter(PlayerInMatch.match_id == self.job.match_id). \
    #                 all():
    #             if player.player.current_match == self.job.match_id:
    #                 player.player.current_match = None
    #             self.players[player.player_id] = player
    #
    #         # Process scoreboard updates
    #         for player_id, player in self.players.items():
    #             score = Scoreboard.query.filter_by(ladder_name=match.section, user_id=player_id).first()
    #             if score is None:
    #                 score = Scoreboard(user=player.player, ladder_name=match.section)
    #                 db.session.add(score)
    #             score.matches += 1
    #         for player in self.game_status.members:
    #             if player.id == self.dota.steam_id:
    #                 continue
    #             id = player.id
    #             score = Scoreboard.query.filter_by(ladder_name=match.section, user_id=id).first()
    #             if (self.players[id].is_radiant and self.game_status.match_outcome == 2) or \
    #                     (not self.players[id].is_radiant and self.game_status.match_outcome == 3):
    #                 score.points += 1
    #                 score.win += 1
    #             elif (self.players[id].is_radiant and self.game_status.match_outcome == 3) or \
    #                     (not self.players[id].is_radiant and self.game_status.match_outcome == 2):
    #                 score.loss += 1
    #         for player in self.game_status.left_members:
    #             score = Scoreboard.query.filter_by(ladder_name=match.section, user_id=player.id).first()
    #             self.players[player.id].is_leaver = True
    #             score.points -= 3
    #             score.leave += 1
    #
    #         db.session.commit()
