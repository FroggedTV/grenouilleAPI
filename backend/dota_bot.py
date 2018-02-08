import logging
import enum
import random
from gevent import Greenlet, sleep

from steam import SteamClient, SteamID
import dota2
from dota2.enums import DOTA_GC_TEAM, DOTA_CM_PICK, EMatchOutcome

from app import create_app
from models import db, Game, GameStatus

class DotaBotState(enum.Enum):
    STARTING = 0
    HOSTING_GAME = 1
    SETUP_GAME = 2
    WAITING_FOR_PLAYERS = 3
    PICKING_SIDE_ORDER = 4
    WAITING_FOR_READY = 5
    LOADING_GAME = 6
    RETRY_WAITING_FOR_READY = 7
    GAME_IN_PROGRESS = 8
    GAME_FINISHED = 9

    FINISHED = 100


class DotaBot(Greenlet):
    """A worker thread, connecting to steam to process a unique job.

    Attributes:
        worker_manager: `WorkerManager` this bot is linked to.
        credential: `Credential` used to connect to steam.
    """

    def __init__(self, worker_manager, credential, admins, casters, id, name, password, team1, team2, team1_ids, team2_ids,
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
        self.admins = admins
        self.casters = casters
        self.lobby_options = {
            'game_name': self.name,
            'pass_key': self.password,
            'game_mode': dota2.enums.DOTA_GameMode.DOTA_GAMEMODE_CM,
            'server_region': int(dota2.enums.EServerRegion.Europe),
            'fill_with_bots': False,
            'allow_spectating': True,
            #'allow_cheats': False,
            'allow_cheats': True,
            'allchat': False,
            'dota_tv_delay': 2,
            'pause_setting': 1,
            #'leagueid': 4947 # FTV LEAGUE SEASON 1
            #'leagueid': 9674 # FTV LEAGUE SEASON 2
        }

        # Choices
        self.team_choosing_first = team_choosing_first
        self.team_choosing_now = team_choosing_first
        self.team_choices = [None, None]
        self.team_choices_possibilities = ['!radiant', '!dire', '!fp', '!sp']
        self.team_inverted = False

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

        while self.machine_state != DotaBotState.SETUP_GAME:
            sleep(5)
        self.initialize_lobby()
        sleep(10) # Wait for setup

        remaining_time = 1800 # Attente 30 min au max

        # P1: Wait for people to join for 25 minutes, P2 if slots are filled (X=min remaining )
        self.print_info('Waiting for players.')
        team_names, missing_players = self.check_teams()
        while (remaining_time > 300 and (team_names[0] is False or
                                         team_names[1] is False or
                                         missing_players[0] != 0 or
                                         missing_players[1] != 0)):
            self.display_status(remaining_time, missing_players, team_names)
            sleep(30)
            remaining_time -= 30
            team_names, missing_players = self.check_teams()

        # P2: Give 1min for each teams to pick sides/picks
        self.print_info('Choice side/order.')
        self.machine_state = DotaBotState.PICKING_SIDE_ORDER
        msg = '{0} Choix du side/ordre, team {1} choisit entre {2}.'.format(
            self.remaining_time_to_string(remaining_time),
            self.team_choosing_now,
            ', '.join(self.team_choices_possibilities))
        self.dota.channels.lobby.send(msg)

        team_choice_remaining_time = [60, 60]
        while team_choice_remaining_time[self.team_choosing_now-1]:
            sleep(1)
            remaining_time -= 1
            team_choice_remaining_time[self.team_choosing_now-1] -= 1
            if self.team_choices[self.team_choosing_now-1] is not None:
                break

        if self.team_choices[self.team_choosing_now - 1] is None:
            # RANDOM
            self.team_choices[self.team_choosing_now - 1] = random.choice(self.team_choices_possibilities)[1:]
            msg = '{0} Team {1} a random {2}.'.format(
                self.remaining_time_to_string(remaining_time),
                self.team_choosing_now,
                self.team_choices[self.team_choosing_now - 1])
        else:
            # Choice
            msg = '{0} Team {1} a choisi {2}.'.format(
                self.remaining_time_to_string(remaining_time),
                self.team_choosing_now,
                self.team_choices[self.team_choosing_now - 1])

        self.team_choices_possibilities.remove('!{0}'.format(self.team_choices[self.team_choosing_now - 1]))
        complementary = {
            'fp': '!sp',
            'sp': '!fp',
            'radiant': '!dire',
            'dire': '!radiant'
        }
        self.team_choices_possibilities.remove(complementary[self.team_choices[self.team_choosing_now - 1]])
        self.team_choosing_now = (self.team_choosing_now % 2) + 1
        msg = '{0} Team {1} choisit entre {2}.'.format(
            msg,
            self.team_choosing_now,
            ', '.join(self.team_choices_possibilities))
        self.dota.channels.lobby.send(msg)

        while team_choice_remaining_time[self.team_choosing_now-1]:
            sleep(1)
            remaining_time -= 1
            team_choice_remaining_time[self.team_choosing_now-1] -= 1
            if self.team_choices[self.team_choosing_now-1] is not None:
                break

        if self.team_choices[self.team_choosing_now - 1] is None:
            # RANDOM
            self.team_choices[self.team_choosing_now - 1] = random.choice(self.team_choices_possibilities)[1:]
            msg = '{0} Team {1} a random {2}.'.format(
                self.remaining_time_to_string(remaining_time),
                self.team_choosing_now,
                self.team_choices[self.team_choosing_now - 1])
        else:
            # Choice
            msg = '{0} Team {1} a choisi {2}. Lancement dès que le lobby est complet.'.format(
                self.remaining_time_to_string(remaining_time),
                self.team_choosing_now,
                self.team_choices[self.team_choosing_now - 1])
        self.dota.channels.lobby.send(msg)

        # Config
        if self.team_choices[0] == 'dire' or self.team_choices[1] == 'radiant':
            self.team_inverted = True
            self.dota.flip_lobby_teams()
        if ((self.team_choices[0] == 'fp' and self.team_choices[1] == 'dire') or
            (self.team_choices[0] == 'sp' and self.team_choices[1] == 'radiant') or
            (self.team_choices[0] == 'radiant' and self.team_choices[1] == 'sp') or
            (self.team_choices[0] == 'dire' and self.team_choices[1] == 'fp')):
            self.lobby_options['cm_pick'] = DOTA_CM_PICK.DOTA_CM_GOOD_GUYS
        else:
            self.lobby_options['cm_pick'] = DOTA_CM_PICK.DOTA_CM_BAD_GUYS
        self.dota.config_practice_lobby(options=self.lobby_options)
        self.machine_state = DotaBotState.WAITING_FOR_READY

        # Resync time to modulo 30
        sleep(remaining_time % 30)
        remaining_time -= remaining_time % 30

        # P3: Give min(1, 30-X-2) min for teams to get into slots, starts when both teams ready
        team_names, missing_players = self.check_teams()
        while (remaining_time > 0 and (team_names[0] is False or
                                       team_names[1] is False or
                                       missing_players[0] != 0 or
                                       missing_players[1] != 0)):
            self.display_status(remaining_time, missing_players, team_names)
            sleep(30)
            remaining_time -= 30
            team_names, missing_players = self.check_teams()

        # Cancel lobby test
        if remaining_time <= 0:
            self.print_info('Lobby incomplet, annulation de la game.')
            self.dota.channels.lobby.send('Joueurs manquants, lobby annulé.')
            with self.app.app_context():
                game = db.session().query(Game).filter(Game.id == self.id).one_or_none()
                if game is not None:
                    game.status = GameStatus.CANCELLED
                    db.session().commit()
            sleep(15)
            self.end_bot()

        # Start and retry
        self.dota.channels.lobby.send('Démarrage de la partie...')
        self.machine_state = DotaBotState.LOADING_GAME
        self.dota.launch_practice_lobby()
        while self.machine_state == DotaBotState.LOADING_GAME:
            sleep(5)

        if self.lobby_status.state == 0:
            self.print_info('Erreur lors du chargement, annulation de la game.')
            self.dota.channels.lobby.send('Impossible de charger la partie, game annulée. Contactez un admin.')
            with self.app.app_context():
                game = db.session().query(Game).filter(Game.id == self.id).one_or_none()
                if game is not None:
                    game.status = GameStatus.CANCELLED
                    db.session().commit()
            sleep(15)
            self.end_bot()

        # IN GAME WAIT
        self.print_info('Game in progress...')
        with self.app.app_context():
            game = db.session().query(Game).filter(Game.id == self.id).one_or_none()
            if game is not None:
                game.status = GameStatus.GAME_IN_PROGRESS
                db.session().commit()
        while self.lobby_status.state != 3:
            sleep(30)

        # Game over
        self.machine_state = DotaBotState.GAME_FINISHED
        self.print_info('Game completed.')
        with self.app.app_context():
            game = db.session().query(Game).filter(Game.id == self.id).one_or_none()
            if game is not None:
                game.status = GameStatus.COMPLETED
                game.valve_id = self.lobby_status.match_id
                if ((self.lobby_status.match_outcome == 2 and not self.team_inverted) or
                    (self.lobby_status.match_outcome == 3 and self.team_inverted)):
                    game.winner = 1
                else:
                    game.winner = 2
                db.session().commit()
        self.end_bot()

    def end_bot(self):
        """End the life of the bot."""
        self.print_info('Bot work over.')
        self.machine_state = DotaBotState.FINISHED

        self.dota.destroy_lobby()
        sleep(1)

        self.client.disconnect()
        self.worker_manager.bot_end(self.credential)
        self.kill()

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

        message_steam_id = SteamID(message.account_id).as_64
        # Feature commands
        if command[0] == 'commands':
            self.dota.channels.lobby.send('Commandes: !cocaster, !destroy, !standin')
        elif command[0] == 'philaeux':
            self.dota.channels.lobby.send('Respectez mon créateur ou je vous def lose.')
        elif command[0] == 'cocaster':
            if message_steam_id not in self.admins and message_steam_id not in self.casters:
                self.dota.channels.lobby.send('Seuls les casters et admins peuvent ajouter un cocaster.')
                return
            if len(command) != 2:
                self.dota.channels.lobby.send('!cocaster X où X est le steamID (64bits) du cocaster.')
                return
            if not command[1].isdigit():
                self.dota.channels.lobby.send('SteamID (64bits) invalide dans la commande !cocaster.')
            else:
                self.casters.append(int(command[1]))
                self.dota.channels.lobby.send('Cocaster {0} ajouté.'.format(command[1]))
        elif command[0] == 'standin':
            if message_steam_id not in self.admins:
                self.dota.channels.lobby.send('Seuls les admins peuvent ajouter un standin.')
                return
            if len(command) != 3:
                self.dota.channels.lobby.send("!standin X Y où X est le steamID (64bits) du standin et Y l'équipe (1 ou 2).")
                return
            if not command[1].isdigit():
                self.dota.channels.lobby.send('SteamID (64bits) invalide dans la commande !standin.')
                return
            if command[2] not in ['1', '2']:
                self.dota.channels.lobby.send('Équipe (1 ou 2) invalide dans la commande !standin.')
            else:
                if command[2] == '1':
                    self.team1_ids.append(int(command[1]))
                else:
                    self.team2_ids.append(int(command[1]))
                self.dota.channels.lobby.send("Standin {0} ajouté à l'équipe {1}.".format(command[1], command[2]))
        elif command[0] == 'destroy':
            if message_steam_id not in self.admins:
                self.dota.channels.lobby.send('Seuls les admins peuvent détruirent le lobby.')
            else:
                self.dota.channels.lobby.send('Lobby annulé par un admin.')
                with self.app.app_context():
                    game = db.session().query(Game).filter(Game.id == self.id).one_or_none()
                    if game is not None:
                        game.status = GameStatus.CANCELLED
                        db.session().commit()
                self.end_bot()

        # Main Loop commands
        elif command[0] == 'fp' or command[0] == 'sp' or command[0] == 'radiant' or command[0] == 'dire':
            if '!{0}'.format(command[0]) in self.team_choices_possibilities:
                if self.machine_state == DotaBotState.PICKING_SIDE_ORDER:
                    compare = self.team1_ids if self.team_choosing_now == 1 else self.team2_ids
                    if message_steam_id in compare:
                        self.team_choices[self.team_choosing_now-1] = command[0]

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
        self.machine_state = DotaBotState.SETUP_GAME

    def game_update(self, message):
        """Callback fired when the game lobby change, update local information."""
        self.lobby_status = message
        if self.machine_state == DotaBotState.LOADING_GAME:
            if self.lobby_status.state == 0:
                self.machine_state = DotaBotState.RETRY_WAITING_FOR_READY
            elif self.lobby_status.state == 2:
                if self.lobby_status.game_state not in [0, 1]:
                    self.machine_state = DotaBotState.GAME_IN_PROGRESS

        # Kick players not authorized
        for member in message.members:
            if member.id == self.dota.steam_id:
                continue
            if (member.id not in self.team1_ids and
                member.id not in self.team2_ids and
                member.id not in self.admins and
                member.id not in self.casters):
                self.dota.practice_lobby_kick(SteamID(member.id).as_32)
            if ((member.team == DOTA_GC_TEAM.SPECTATOR) or
                (member.team == DOTA_GC_TEAM.BROADCASTER and not (member.id in self.admins or member.id in self.casters))):
                self.dota.practice_lobby_kick_from_team(SteamID(member.id).as_32)
            else:
                if self.team_inverted:
                    if ((member.team == DOTA_GC_TEAM.BAD_GUYS and member.id not in self.team1_ids) or
                        (member.team == DOTA_GC_TEAM.GOOD_GUYS and member.id not in self.team2_ids)):
                        self.dota.practice_lobby_kick_from_team(SteamID(member.id).as_32)
                else:
                    if ((member.team == DOTA_GC_TEAM.GOOD_GUYS and member.id not in self.team1_ids) or
                        (member.team == DOTA_GC_TEAM.BAD_GUYS and member.id not in self.team2_ids)):
                        self.dota.practice_lobby_kick_from_team(SteamID(member.id).as_32)

    def initialize_lobby(self):
        """Setup the game lobby with the good options, and change status in database."""
        self.print_info('Game hosted, setup.')

        self.dota.channels.join_lobby_channel()
        self.dota.join_practice_lobby_team()
        self.dota.config_practice_lobby(options=self.lobby_options)
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
        if self.team_inverted:
            compare = [self.team2, self.team1]
        else:
            compare = [self.team1, self.team2]
        for team_detail in self.lobby_status.team_details:
            team_names[i] = team_detail.team_id == compare[i]
            i = i+1
        return team_names, missing_players

    def display_status(self, remaining_time, missing_players, team_names):
        """Display status in chat."""
        msg = self.remaining_time_to_string(remaining_time)
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

    @staticmethod
    def remaining_time_to_string(remaining_time):
        return '{0}m{1:02d}s -'.format(remaining_time//60, remaining_time%60)
