import logging
import enum
from gevent import Greenlet, sleep

from steam import SteamClient, SteamID
import dota2
from dota2.enums import DOTA_GC_TEAM, EMatchOutcome

from app import create_app
from models import db, Game, GameStatus

class DotaBotState(enum.Enum):
    STARTING = 0
    HOSTING_GAME = 1
    WAITING_FOR_PLAYERS = 2
    PICKING_SIDE_ORDER = 3
    WAITING_FOR_READY = 4
    LOADING_GAME = 5
    RETRY_WAITING_FOR_READY = 6
    GAME_IN_PROGRESS = 7
    GAME_FINISHED = 8

    FINISHED = 100


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
        self.vips = []
        self.team_choosing_first = team_choosing_first

        # State machine variables
        self.machine_state = DotaBotState.STARTING
        self.lobby_status = {}

        """
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
        self.dota.channels.on(dota2.features.chat.ChannelManager.EVENT_JOINED_CHANNEL, self.channel_join)
        self.dota.channels.on(dota2.features.chat.ChannelManager.EVENT_MESSAGE, self.channel_message)


    def _run(self):
        """Start the main loop of the thread, connecting to Steam, waiting for the job to finish to close the bot."""
        self.print_info('Connecting to Steam...')
        self.client.connect(retry=None)  # Try connecting with infinite retries

        while self.machine_state != DotaBotState.FINISHED:
            sleep(30)

        self.client.disconnect()
        self.worker_manager.bot_end(self.credential)

    def end_bot(self):
        """End the life of the bot."""
        self.print_info('Bot work over.')
        self.dota.destroy_lobby()
        self.dota.leave_practice_lobby()
        self.machine_state = DotaBotState.FINISHED

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
    def channel_join(self, channel_info):
        pass
        #self.print_info('Channel join! {0}'.format(channel_info))
        """
        if channel_info.channel_type != dota2.enums.DOTAChatChannelType_t.DOTAChannelType_Lobby:
            self.dota.leave_channel(channel_info.channel_id)
        else:
            if self.game_status is not None:
                if channel_info.channel_name == 'Lobby_{0}'.format(self.game_status.lobby_id):
                    self.lobby_channel_id = channel_info.channel_id"""

    def channel_message(self, channel, message):
        if message.text[0] != '!':
            return
        command = message.text[1:].strip().split(' ')
        if len(command) == 0:
            return
        if command[0] == 'philaeux':
            self.dota.channels.lobby.send('Respectez mon créateur ou je vous def lose.')
        elif command[0] == 'autodestruction':
            self.end_bot()

    # Hosting events
    def host_game(self):
        """Start the processing of the job with the appropriate handler."""
        self.print_info('Hosting game {0} with password {1}'.format(self.name, self.password))
        self.machine_state = DotaBotState.HOSTING_GAME
        self.dota.create_practice_lobby(password=self.password)

    def game_hosted(self, message):
        """Callback fired when the Dota bot enters a lobby."""
        if self.machine_state != DotaBotState.HOSTING_GAME:
            self.dota.destroy_lobby()
            self.dota.leave_practice_lobby() # Sometimes the bot get back to an old lobby at startup
            return

        self.lobby_status = message
        self.initialize_lobby()

        sleep(10) # Wait for setup

        refresh_rate = 30
        remaining_time = 1800

        # P1: Wait for people to join for 25 minutes, P2 if slots are filled (X=min remaining )
        self.print_info('P1: Waiting for players.')
        team_names, missing_players = self.check_teams()
        while (remaining_time > 300 and (team_names[0] is False or
                                         team_names[1] is False or
                                         missing_players[0] != 0 or
                                         missing_players[1] != 0)):
            self.display_status(remaining_time, missing_players, team_names)
            sleep(refresh_rate)
            remaining_time = remaining_time - refresh_rate
            team_names, missing_players = self.check_teams()

        # P2: Give 1min for each teams to pick sides/picks

        # P3: Give min(1, 30-X-2) min for teams to get into slots, starts when both teams ready, or time passed

        # P4: wait for game to finish

        # P5: report results
        self.end_bot()

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

        # Kick players not authorized
        for member in message.members:
            if member.id == self.dota.steam_id:
                continue
            if (member.id not in self.team1_ids and
                member.id not in self.team2_ids and
                member.id not in self.vips):
                self.dota.practice_lobby_kick(SteamID(member.id).as_32)
            if ((member.team == DOTA_GC_TEAM.GOOD_GUYS and member.id not in self.team1_ids) or
                (member.team == DOTA_GC_TEAM.BAD_GUYS and member.id not in self.team2_ids) or
                (member.team == DOTA_GC_TEAM.SPECTATOR) or
                (member.team == DOTA_GC_TEAM.BROADCASTER and member.id not in self.vips)):
                self.dota.practice_lobby_kick_from_team(SteamID(member.id).as_32)

    def initialize_lobby(self):
        """Setup the game lobby with the good options, and change status in database."""
        self.print_info('Game hosted, setup.')

        self.dota.channels.join_lobby_channel()
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
            'pause_setting': 1,
            'leagueid': 4947
        }
        self.dota.config_practice_lobby(options=options)
        with self.app.app_context():
            game = db.session().query(Game).filter(Game.id == self.id).one_or_none()
            if game is not None:
                game.status = GameStatus.WAITING_FOR_PLAYERS
                db.session().commit()
        self.machine_state = DotaBotState.WAITING_FOR_PLAYERS

    def check_teams(self):
        """Check team players and team names."""
        missing_players = [min(5, len(self.team1_ids)), min(5, len(self.team2_ids))]
        team_names = [False, False]

        for member in self.lobby_status.members:
            if member.team == DOTA_GC_TEAM.GOOD_GUYS:
                missing_players[0] = missing_players[0] - 1
            elif member.team == DOTA_GC_TEAM.BAD_GUYS:
                missing_players[1] = missing_players[1] - 1
        i = 0
        compare = [self.team1, self.team2]
        for team_detail in self.lobby_status.team_details:
            team_names[i] = team_detail.team_id == compare[i]
            i = i+1
        return team_names, missing_players

    def display_status(self, remaining_time, missing_players, team_names):
        """Display status in chat."""
        msg = '{0}m{1:02d}s -'.format(remaining_time//60, remaining_time%60)
        if not team_names[0]:
            msg = msg + " Le Radiant n'a pas la bonne team."
        if missing_players[0] == 1:
            msg = msg + " 1 joueur Radiant manquant."
        elif missing_players[0] > 1:
            msg = msg + " {0} joueurs Radiant manquants.".format(missing_players[0])
        if not team_names[1]:
            msg = msg + " Le Dire n'a pas la bonne team."
        if missing_players[1] == 1:
            msg = msg + " 1 joueur Dire manquant."
        elif missing_players[1] > 1:
            msg = msg + " {0} joueurs Dire manquants.".format(missing_players[1])
        self.dota.channels.lobby.send(msg)

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
