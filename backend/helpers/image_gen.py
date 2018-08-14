from itertools import chain
import logging
import math
import requests
import json
import csv
import os
from io import StringIO
from sqlalchemy import desc

from PIL import Image, ImageDraw, ImageColor, ImageFont

from models import db, CSVData, DotaHero, DotaItem, DotaProPlayer, DotaProTeam, DotaStatTounamentHero

class ImageGenerator:
    """Class helper to generate stats images.

    Attributes:
        app: Flask application.
        colors: Colors used in multiple points of the application.
    """
    app = None
    colors = {
        'hero_blue': ImageColor.getrgb('#3375ff'),
        'hero_teal': ImageColor.getrgb('#65fdbd'),
        'hero_purple': ImageColor.getrgb('#bf00bf'),
        'hero_yellow': ImageColor.getrgb('#f3f00b'),
        'hero_orange': ImageColor.getrgb('#ff6b00'),
        'hero_pink': ImageColor.getrgb('#fc85c0'),
        'hero_grey': ImageColor.getrgb('#a0b346'),
        'hero_aqua': ImageColor.getrgb('#65d9f7'),
        'hero_green': ImageColor.getrgb('#008321'),
        'hero_brown': ImageColor.getrgb('#a46900'),
        'white': ImageColor.getrgb('#ffffff'),
        'ti_green': ImageColor.getrgb('#83a94c'),
        'black': ImageColor.getrgb('#000000'),
        'orange': ImageColor.getrgb('#ff6a38'),
        'yellow': ImageColor.getrgb('#FFDF00'),
        'blue': ImageColor.getrgb('#00c8ff'),
        'grey': ImageColor.getrgb('#cecece'),
        'light_blue': ImageColor.getrgb('#4C83A9'),
        'light_red': ImageColor.getrgb('#E75348'),
        'light_grey': ImageColor.getrgb('#aaaaaa')
    }

    def __init__(self, app):
        self.app = app

    def generate_image(self, key, payload):
        """Generate images of a target CSV key.

        Args:
            key: CSV key to generate.
            payload: Payload information for image generation
        """
        if key == "preti8_teams":
            self.generate_csv_preti8_teams(payload['team_id'])
        elif key == "preti8_players":
            self.generate_csv_preti8_players(payload['player_id'])
        elif key == "ti8_groups":
            self.generate_csv_ti8_groups()
        elif key == "post_game":
            self.generate_post_game(payload['match_id'])
        elif key == "tournament_global":
            self.generate_tournament_global(payload['tournament_id'])
        elif key == "team_faceoff":
            self.generate_team_faceoff(payload['team_id'], payload['team_id_2'])

    def generate_csv_preti8_teams(self, team_id = None):
        csv_data = db.session.query(CSVData).filter(CSVData.key=='preti8_teams').one_or_none()
        if csv_data is None: return;

        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}
        for row in csv_reader:
            if team_id is not None and team_id != row[header['teamid']]:
                continue

            # Delete previous image
            image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'preti8_teams-' + row[header['teamid']] + '.png')
            if os.path.isfile(image_path): os.remove(image_path)

            # Generate image
            composition = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'preti8_teams-background.png')).convert('RGBA')

            logo_array = {
                '5': { 'position': [400, 650], 'size': [None, 700], 'suffix': ''},
                '15': { 'position': [300, 650], 'size': [None, 700], 'suffix': '' },
                '39': { 'position': [400, 650], 'size': [None, 600], 'suffix': '' },
                '67': { 'position': [400, 650], 'size': [None, 600], 'suffix': '' },
                '2163': { 'position': [400, 650], 'size': [None, 600], 'suffix': '' },
                '350190': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '543897': { 'position': [400, 700], 'size': [None, 700], 'suffix': '' },
                '726228': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '1375614': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '1838315': { 'position': [400, 650], 'size': [None, 500], 'suffix': '' },
                '1883502': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '2108395': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '2586976': { 'position': [350, 650], 'size': [None, 700], 'suffix': '' },
                '5026801': { 'position': [375, 630], 'size': [None, 700], 'suffix': '-white' },
                '5027210': { 'position': [400, 700], 'size': [None, 700], 'suffix': '-white' },
                '5066616': { 'position': [400, 700], 'size': [None, 500], 'suffix': '' },
                '5228654': { 'position': [350, 650], 'size': [None, 700], 'suffix': '-white' },
                '5229127': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
            }
            composition = self.draw_team_logo(composition,
                                              row[header['teamid']] + logo_array[row[header['teamid']]]['suffix'],
                                              logo_array[row[header['teamid']]]['position'],
                                              logo_array[row[header['teamid']]]['size'],
                                              0.7)
            image_draw = ImageDraw.Draw(composition)

            rift_bold_title = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 150)
            rift_bold_sub = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 58)
            rift_player_nickname = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_regular_italic.otf'), 72)
            self.draw_text_outlined(image_draw, [85, 51], row[header['team']], font=rift_bold_title, fill=self.colors['ti_green'], outline_fill=self.colors['black'], outline_width=5)

            row_1_x = 800
            row_1_y = 350
            row_1_line = 65
            row_1_inc = 225
            row_2_x = row_1_x + 40
            row_2_y = 330
            row_2_inc = 225
            row_3_x = 1400
            row_4_x = row_3_x + 40
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y], 'Classement', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_line], 'DPC', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_inc], 'Points DPC', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_inc + row_1_line], 'Obtenus', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + 2*row_1_inc], 'Games', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + 2*row_1_inc + row_1_line], '4 Mois -', rift_bold_sub, self.colors['white'])
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y-5], row[header['classement_dpc']], font=rift_bold_title, fill=self.colors['ti_green'],
                                    outline_fill=self.colors['black'], outline_width=5)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y + row_2_inc-5], row[header['total_dpc']], font=rift_bold_title, fill=self.colors['ti_green'],
                                    outline_fill=self.colors['black'], outline_width=5)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y + 2*row_2_inc-5], row[header['nombre_games']], font=rift_bold_title, fill=self.colors['ti_green'],
                                    outline_fill=self.colors['black'], outline_width=5)

            self.draw_text_left_align(image_draw, [row_3_x, row_1_y], 'Winrate', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_3_x, row_1_y + row_1_line], '4 mois -', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_3_x, row_1_y + row_1_inc], 'Gains', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_3_x, row_1_y + row_1_inc + row_1_line], 'saison -', rift_bold_sub, self.colors['white'])
            self.draw_text_outlined(image_draw, [row_4_x, row_2_y-5], row[header['wr']] + ' %', font=rift_bold_title, fill=self.colors['ti_green'],
                                    outline_fill=self.colors['black'], outline_width=5)
            self.draw_text_outlined(image_draw, [row_4_x, row_2_y + row_2_inc-5], '$ ' + row[header['gains']], font=rift_bold_title, fill=self.colors['ti_green'],
                                    outline_fill=self.colors['black'], outline_width=5)

            players = db.session.query(DotaProPlayer).filter(DotaProPlayer.team == int(row[header['teamid']])).all()
            player_string = ''
            for i in range(0, 5):
                player_string += '     {0}'.format(players[i].nickname)
            player_string += '   '
            self.draw_text_center_align(image_draw, [960, 230], text=player_string, font=rift_player_nickname, fill=self.colors['white'])

            composition.save(image_path)

    def generate_csv_preti8_players(self, player_id = None):
        csv_data = db.session.query(CSVData).filter(CSVData.key == 'preti8_players').one_or_none()
        if csv_data is None: return;

        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}
        for row in csv_reader:
            if (len(row[header['playerid']]) == 0 or (not row[header['playerid']].isdigit()) or
                    (player_id is not None and player_id != row[header['playerid']])):
                continue

            # Delete previous image
            image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'preti8_players-' + row[header['playerid']] + '.png')
            if os.path.isfile(image_path): os.remove(image_path)

            # Generate image
            composition = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'preti8_players-background.png')).convert('RGBA')
            logo_array = {
                '5': { 'position': [400, 650], 'size': [None, 700], 'suffix': ''},
                '15': { 'position': [300, 650], 'size': [None, 700], 'suffix': '' },
                '39': { 'position': [400, 650], 'size': [None, 600], 'suffix': '' },
                '67': { 'position': [400, 650], 'size': [None, 600], 'suffix': '' },
                '2163': { 'position': [400, 650], 'size': [None, 600], 'suffix': '' },
                '350190': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '543897': { 'position': [400, 700], 'size': [None, 700], 'suffix': '' },
                '726228': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '1375614': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '1838315': { 'position': [400, 650], 'size': [None, 500], 'suffix': '' },
                '1883502': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '2108395': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
                '2586976': { 'position': [350, 650], 'size': [None, 700], 'suffix': '' },
                '5026801': { 'position': [375, 630], 'size': [None, 700], 'suffix': '-white' },
                '5027210': { 'position': [400, 700], 'size': [None, 700], 'suffix': '-white' },
                '5066616': { 'position': [400, 700], 'size': [None, 500], 'suffix': '' },
                '5228654': { 'position': [350, 650], 'size': [None, 700], 'suffix': '-white' },
                '5229127': { 'position': [400, 650], 'size': [None, 700], 'suffix': '' },
            }
            composition = self.draw_team_logo(composition,
                                              row[header['teamid']] + logo_array[row[header['teamid']]]['suffix'],
                                              logo_array[row[header['teamid']]]['position'],
                                              logo_array[row[header['teamid']]]['size'],
                                              0.7)
            composition = self.draw_player_portrait(composition, row[header['playerid']], position=[400, 780], size=[None, 600])
            image_draw = ImageDraw.Draw(composition)

            rift_bold_title = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 150)
            rift_bold_sub = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 58)

            self.draw_text_outlined(image_draw, [85, 51], row[header['pseudo']], font=rift_bold_title, fill=self.colors['ti_green'], outline_fill=self.colors['black'], outline_width=5)
            image_draw.text([85, 215], row[header['team']], font=rift_bold_sub, fill=self.colors['white'])

            row_1_x = 950
            row_1_y = 350
            row_1_line = 65
            row_1_inc = 225
            row_2_x = row_1_x + 40
            row_2_y = 330
            row_2_inc = 225
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y], 'Héros du', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_line], 'Moment', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_inc], 'Networth', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_inc + row_1_line], "Dans l'équipe", rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + 2*row_1_inc], 'Nombre de', rift_bold_sub, self.colors['white'])
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + 2*row_1_inc + row_1_line], 'héros joués', rift_bold_sub, self.colors['white'])
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y-5], row[header['hero_privilegie']].replace('_', ' '), font=rift_bold_title, fill=self.colors['ti_green'],
                                    outline_fill=self.colors['black'], outline_width=5)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y + row_2_inc-5], row[header['networth']] + ' %', font=rift_bold_title, fill=self.colors['ti_green'],
                                    outline_fill=self.colors['black'], outline_width=5)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y + 2*row_2_inc-5], row[header['nombre_heros']], font=rift_bold_title, fill=self.colors['ti_green'],
                                    outline_fill=self.colors['black'], outline_width=5)

            composition = self.draw_minimap_hero(composition, row[header['hero_signature_1']], [1450, 130], [None, 150])
            composition = self.draw_minimap_hero(composition, row[header['hero_signature_2']], [1600, 130], [None, 150])
            composition = self.draw_minimap_hero(composition, row[header['hero_signature_3']], [1750, 130], [None, 150])

            composition.save(image_path)

    def generate_csv_ti8_groups(self):
        csv_data = db.session.query(CSVData).filter(CSVData.key == 'ti8_groups').one_or_none()
        if csv_data is None: return;

        # Manage data
        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}

        # Delete previous image
        image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'ti8_groups.png')
        if os.path.isfile(image_path): os.remove(image_path)

        # Generate image
        composition = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'ti8_group-background.png')).convert('RGBA')
        image_draw = ImageDraw.Draw(composition)

        rift_bold_title = ImageFont.truetype(
            os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'),
            120)
        rift_regular_sub = ImageFont.truetype(
            os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_regular.otf'),
            58)
        rift_bold_sub = ImageFont.truetype(
            os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'),
            58)

        status_colors = { 'red': self.colors['light_red'], 'green': self.colors['ti_green'], 'blue': self.colors['light_blue'], 'grey': self.colors['light_grey'] }
        logo_array = {
            '5': {'offset': [100, 45], 'size': [None, 65], 'suffix': ''},
            '15': {'offset': [100, 45], 'size': [None, 75], 'suffix': '-horiz'},
            '39': {'offset': [100, 45], 'size': [None, 70], 'suffix': ''},
            '67': {'offset': [100, 45], 'size': [None, 90], 'suffix': '-white'},
            '2163': {'offset': [100, 45], 'size': [None, 75], 'suffix': '-solid'},
            '350190': {'offset': [100, 45], 'size': [None, 65], 'suffix': ''},
            '543897': {'offset': [100, 45], 'size': [None, 75], 'suffix': ''},
            '726228': {'offset': [100, 45], 'size': [None, 70], 'suffix': ''},
            '1375614': {'offset': [100, 45], 'size': [None, 65], 'suffix': ''},
            '1838315': {'offset': [100, 45], 'size': [None, 50], 'suffix': ''},
            '1883502': {'offset': [100, 45], 'size': [None, 65], 'suffix': ''},
            '2108395': {'offset': [100, 45], 'size': [None, 65], 'suffix': ''},
            '2586976': {'offset': [100, 45], 'size': [None, 65], 'suffix': ''},
            '5026801': {'offset': [100, 45], 'size': [None, 75], 'suffix': '-white'},
            '5027210': {'offset': [100, 45], 'size': [None, 75], 'suffix': '-noname'},
            '5066616': {'offset': [100, 45], 'size': [None, 60], 'suffix': ''},
            '5228654': {'offset': [100, 45], 'size': [None, 75], 'suffix': '-noname'},
            '5229127': {'offset': [100, 45], 'size': [None, 100], 'suffix': ''},
        }

        self.draw_text_outlined_center_align(image_draw, [480, 45], 'Groupe A', font=rift_bold_title, fill=self.colors['ti_green'], outline_fill=self.colors['black'], outline_width=5)
        self.draw_text_outlined_center_align(image_draw, [1440, 45], 'Groupe B', font=rift_bold_title, fill=self.colors['ti_green'], outline_fill=self.colors['black'], outline_width=5)

        # Draw
        rectangle_height = 90
        rectangle_start = 215
        rectangle_group_x_start = [100, 1060]
        rectangle_group_x_end = [860, 1820]
        rectangle_padding = 7

        group_a_y = rectangle_start
        group_b_y = rectangle_start
        team_offset = [190, 10]
        win_offset = [615, 10]
        loses_offset = [705, 10]

        for row in csv_reader:
            if row[header['group']] == 'a':
                current_team_x_start = rectangle_group_x_start[0]
                current_team_x_end = rectangle_group_x_end[0]
                current_team_y = group_a_y
            else:
                current_team_x_start = rectangle_group_x_start[1]
                current_team_x_end = rectangle_group_x_end[1]
                current_team_y = group_b_y

            composition = self.draw_alpha_rectangle(composition,
                                                    [current_team_x_start,
                                                     current_team_y + rectangle_padding,
                                                     current_team_x_end,
                                                     current_team_y + rectangle_height - rectangle_padding],
                                                    fill=status_colors[row[header['color']]],
                                                    alpha=0.5)
            image_draw = ImageDraw.Draw(composition)

            image_draw.text([current_team_x_start + team_offset[0], current_team_y + team_offset[1]], row[header['team']], font=rift_regular_sub, fill=self.colors['white'])
            self.draw_text_center_align(image_draw, [current_team_x_start + win_offset[0], current_team_y + win_offset[1]], row[header['wins']], font=rift_bold_sub, fill=self.colors['white'])
            self.draw_text_center_align(image_draw, [current_team_x_start + loses_offset[0], current_team_y + loses_offset[1]], row[header['loses']], font=rift_bold_sub, fill=self.colors['white'])
            composition = self.draw_team_logo(composition,
                                              row[header['teamid']] + logo_array[row[header['teamid']]]['suffix'],
                                              [current_team_x_start + logo_array[row[header['teamid']]]['offset'][0], current_team_y + logo_array[row[header['teamid']]]['offset'][1]],
                                              logo_array[row[header['teamid']]]['size'], 1)

            if row[header['group']] == 'a':
                group_a_y += rectangle_height
            else:
                group_b_y += rectangle_height

        composition.save(image_path)

    def generate_post_game(self, match_id):
        json = self.download_opendata_if_necessary(self.app.config['JSON_CACHE_PATH'], match_id)
        if json is None or json['version'] is None:
            return
        heroes = db.session.query(DotaHero).all()
        items = db.session.query(DotaItem).all()
        players = db.session.query(DotaProPlayer).all()
        teams = db.session.query(DotaProTeam).all()

        # Delete previous image
        image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'post_game-{0}.png'.format(match_id))
        if os.path.isfile(image_path): os.remove(image_path)

        # Generate image
        composition = Image.open(
            os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'post_game-background.png')).convert('RGBA')

        hero_x = 350
        hero_y_side_padding = 30
        hero_height = 90
        hero_width = int(256*hero_height/144)
        hero_y_padding = 10
        item_padding = 4
        item_height = int((hero_height-item_padding)/2)
        item_width = int(88*item_height/64)
        player_name_x_padding = -40
        player_name_y_padding = 0
        player_nickname_y_padding = 50
        kda_padding_x = 5
        hero_y = {0: hero_y_side_padding,
                  1: hero_y_side_padding + hero_height + hero_y_padding,
                  2: hero_y_side_padding + 2*(hero_height + hero_y_padding),
                  3: hero_y_side_padding + 3*(hero_height + hero_y_padding),
                  4: hero_y_side_padding + 4*(hero_height + hero_y_padding),
                  128: 1080 - hero_y_side_padding - hero_height*5 - hero_y_padding*4,
                  129: 1080 - hero_y_side_padding - hero_height*4 - hero_y_padding*3,
                  130: 1080 - hero_y_side_padding - hero_height*3 - hero_y_padding*2,
                  131: 1080 - hero_y_side_padding - hero_height*2 - hero_y_padding,
                  132: 1080 - hero_y_side_padding - hero_height}
        hero_color = {0: self.colors['hero_blue'],
                      1: self.colors['hero_teal'],
                      2: self.colors['hero_purple'],
                      3: self.colors['hero_yellow'],
                      4: self.colors['hero_orange'],
                      128: self.colors['hero_pink'],
                      129: self.colors['hero_grey'],
                      130: self.colors['hero_aqua'],
                      131: self.colors['hero_green'],
                      132: self.colors['hero_brown']}
        hero_color_width = 10

        # Draw Heroes & Items
        for player in json['players']:
            hero = next((hero for hero in heroes if hero.id == player['hero_id']), None)
            if hero is None:
                short_name = 'error'
            else:
                short_name = hero.short_name
            hero_image = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img',
                                                'hero_rectangle', short_name + '.png')).convert('RGBA')
            self.draw_image(composition, hero_image, [hero_x, hero_y[player['player_slot']]], [None, hero_height])
            for j in range(0, 2):
                for i in range(0, 3):
                    key = 'item_{0}'.format(j*3 + i)
                    if player[key] != 0:
                        item = next((item for item in items if item.id == player[key]), None)
                        if item is None:
                            short_name = 'error'
                        else:
                            short_name = item.short_name
                        item_image = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img',
                                                             'item_rectangle', short_name + '.png')).convert('RGBA')
                    else:
                        item_image = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img',
                                                             'item_rectangle', 'empty.png')).convert('RGBA')
                    self.draw_image(composition,
                                    item_image,
                                    [hero_x + hero_width + (i+1)*item_padding + i*item_width,
                                     hero_y[player['player_slot']] + j*(item_height+item_padding)],
                                        [None, item_height])
            # Draw damage sword
            sword_image = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'icon', 'sword.png')).convert('RGBA')
            sword_image = sword_image.resize([int(item_height/2), int(item_height/2)], Image.LANCZOS)
            in_place_sword = Image.new('RGBA', (composition.size[0], composition.size[1]))
            in_place_sword.paste(sword_image,
                                box=[hero_x + hero_width + 3*(item_width + item_padding + kda_padding_x),
                                     hero_y[player['player_slot']] + item_height + 15],
                                mask=sword_image)
            composition = Image.alpha_composite(composition, in_place_sword)

            # Draw kda skull
            skull_image = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'icon', 'skull.png')).convert('RGBA')
            skull_image = skull_image.resize([int(item_height/2), int(item_height/2)], Image.LANCZOS)
            in_place_skull = Image.new('RGBA', (composition.size[0], composition.size[1]))
            in_place_skull.paste(skull_image,
                                box=[hero_x + hero_width + 3*(item_width + item_padding + kda_padding_x),
                                     hero_y[player['player_slot']] + 12],
                                mask=skull_image)
            composition = Image.alpha_composite(composition, in_place_skull)

        # Draw colors
        image_draw = ImageDraw.Draw(composition)
        for player in json['players']:
            image_draw.rectangle([hero_x-hero_color_width,
                                  hero_y[player['player_slot']],
                                  hero_x,
                                  hero_y[player['player_slot']] + hero_height-1],
                                 fill=hero_color[player['player_slot']])

        # Draw player names & pseudo
        rift_player_nickname = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources',
                                              'fonts', 'rift', 'fort_foundry_rift_bold_italic.otf'), 46)
        rift_player_name = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources',
                                              'fonts', 'rift', 'fort_foundry_rift_regular.otf'), 26)
        rift_kda = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources',
                                              'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 32)
        rift_dmg = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources',
                                              'fonts', 'rift', 'fort_foundry_rift_regular.otf'), 32)
        for player in json['players']:
            pro_player = next((pro_player for pro_player in players if pro_player.id == player['account_id']), None)
            if pro_player is None:
                name = '-'
                nickname = '-'
            else:
                name = pro_player.name
                nickname = pro_player.nickname

            self.draw_text_left_align(image_draw, [hero_x + player_name_x_padding,
                                                   hero_y[player['player_slot']] + player_name_y_padding],
                                      nickname, rift_player_nickname, fill=self.colors['white'])
            self.draw_text_left_align(image_draw, [hero_x + player_name_x_padding,
                                                   hero_y[player['player_slot']] + player_name_y_padding + player_nickname_y_padding],
                                      name, rift_player_name, fill=self.colors['white'])
            kda = "{0}/{1}/{2}".format(player['kills'], player['deaths'], player['assists'])
            image_draw.text([hero_x + hero_width + 3*(item_width + item_padding + kda_padding_x) + int(item_height/2) + item_padding,
                             hero_y[player['player_slot']]],
                            text=kda, font=rift_kda, fill=self.colors['white'])
            image_draw.text([hero_x + hero_width + 3*(item_width + item_padding + kda_padding_x) + int(item_height/2) + item_padding,
                             hero_y[player['player_slot']] + item_height + item_padding],
                            text=str(player['hero_damage']), font=rift_dmg, fill=self.colors['orange'])

        # Draw graph
        radiant_gold_adv = json['radiant_gold_adv']
        radiant_xp_adv = json['radiant_xp_adv']
        graph_start_x = 875
        graph_end_x = 1800
        graph_y = 400
        graph_width = 4
        graph_graduation_x = 10

        gold_xp_max = 0
        for item in chain(radiant_gold_adv, radiant_xp_adv):
            if abs(item) > gold_xp_max: gold_xp_max = abs(item)
        gold_xp_max = int((gold_xp_max - gold_xp_max % 1000)/1000 + 1)
        duration = math.ceil(json['duration'] / 60)
        graph_x_step = math.floor((graph_end_x-graph_start_x)/duration)
        graph_y_step = math.floor(graph_y/gold_xp_max)

        image_draw.line([graph_start_x, 540 - int(graph_width/2), graph_end_x, 540 - int(graph_width/2)], fill=self.colors['white'], width=graph_width)
        image_draw.line([graph_start_x - int(graph_width/2), 540-graph_y, graph_start_x - int(graph_width/2), 540+graph_y], fill=self.colors['white'], width=graph_width)
        i = 5
        while i < gold_xp_max:
            image_draw.line([graph_start_x,
                             540 + graph_y_step*i,
                             graph_end_x,
                             540 + graph_y_step*i],
                            fill=self.colors['grey'], width=1)
            image_draw.line([graph_start_x,
                             540 - graph_y_step*i,
                             graph_end_x,
                             540 - graph_y_step*i],
                            fill=self.colors['grey'], width=1)
            i += 5
        i = 5
        while i < duration:
            image_draw.line([graph_start_x + i * graph_x_step,
                             540 - graph_graduation_x-2,
                             graph_start_x + i * graph_x_step,
                             540 + graph_graduation_x-1],
                            fill=self.colors['white'], width=graph_width)
            i += 5
        for i in range(1, duration):
            image_draw.line([graph_start_x + (i-1)*graph_x_step,
                             540 - int(graph_y_step*(radiant_xp_adv[i-1]/1000)),
                             graph_start_x + i*graph_x_step,
                             540 - int(graph_y_step*(radiant_xp_adv[i]/1000))], fill=self.colors['blue'], width=6)
            image_draw.line([graph_start_x + (i-1)*graph_x_step,
                             540 - int(graph_y_step*(radiant_gold_adv[i-1]/1000)),
                             graph_start_x + i*graph_x_step,
                             540 - int(graph_y_step*(radiant_gold_adv[i]/1000))], fill=self.colors['yellow'], width=6)

        for objectif in json['objectives']:
            objectif_x = 0
            objectif_y = 0
            image = 'error'
            if objectif['type'] in ['CHAT_MESSAGE_COURIER_LOST', 'building_kill', 'CHAT_MESSAGE_ROSHAN_KILL']:
                objectif_x = graph_start_x + int(graph_x_step * objectif['time'] / 60)
                if objectif['type'] == 'CHAT_MESSAGE_COURIER_LOST':
                    image = 'chick_kill'
                    if objectif['team'] == 2:
                        objectif_y = 540 - graph_y - 35
                    else:
                        objectif_y = 540 + graph_y + 35
                elif objectif['type'] == 'CHAT_MESSAGE_ROSHAN_KILL':
                    image = 'roshan_kill'
                    if objectif['team'] == 2:
                        objectif_y = 540 - graph_y - 35
                    else:
                        objectif_y = 540 + graph_y + 35
                else:
                    if 'badguys' in objectif['key']:
                        objectif_y = 540 - graph_y - 35
                    else:
                        objectif_y = 540 + graph_y + 35
                    if 'tower' in objectif['key']:
                        image = 'tower_kill'
                    elif 'healers' in objectif['key']:
                        image = 'shrine_kill'
                    elif 'melee_rax' in objectif['key']:
                        image = 'rax_kill'
            if image == 'error':
                continue

            image_icon = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'icon', image + '.png')).convert('RGBA')
            composition = self.draw_image_centered(composition, image_icon, [objectif_x, objectif_y], [35, 35])
        for player in json['players']:
            for item_purchase in player['purchase_log']:
                if item_purchase['key'] in ['black_king_bar', 'blink', 'sheepstick', 'silver_edge', 'refresher', 'orchid']:
                    if player['player_slot'] > 100:
                        item_y = 540 + graph_y
                    else:
                        item_y = 540 - graph_y
                    item_x = graph_start_x + int(graph_x_step * item_purchase['time'] / 60)

                    image_icon = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'icon', 'item_' + item_purchase['key'] + '.png')).convert('RGBA')
                    composition = self.draw_image_centered(composition, image_icon, [item_x, item_y], [35, 35])

        image_draw = ImageDraw.Draw(composition)
        radiant_team = '?'
        dire_team = '?'
        radiant_team_info = next((team for team in teams if team.id == json['radiant_team_id']), None)
        if radiant_team_info is not None:
            radiant_team = radiant_team_info.name
        dire_team_info = next((team for team in teams if team.id == json['dire_team_id']), None)
        if dire_team_info is not None:
            dire_team = dire_team_info.name

        rift_team = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 50)
        radiant_color = self.colors['ti_green']
        dire_color = self.colors['ti_green']
        laurels_icon = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'icon', 'laurels.png')).convert('RGBA')
        if json['radiant_win']:
            laurels_x =[int((graph_start_x + graph_end_x - image_draw.textsize(radiant_team, rift_team)[0])/2) - 40,
                        int((graph_start_x + graph_end_x + image_draw.textsize(radiant_team, rift_team)[0])/2) + 40]
            laurels_y = 45
            dire_color = self.colors['grey']
        else:
            laurels_x =[int((graph_start_x + graph_end_x - image_draw.textsize(dire_team, rift_team)[0])/2) - 40,
                        int((graph_start_x + graph_end_x + image_draw.textsize(dire_team, rift_team)[0])/2) + 40]
            laurels_y = 1035
            radiant_color = self.colors['grey']
        self.draw_text_outlined_center_align(image_draw, [int((graph_start_x + graph_end_x)/2), 15], radiant_team, font=rift_team, fill=radiant_color, outline_fill=self.colors['black'], outline_width=4)
        self.draw_text_outlined_center_align(image_draw, [int((graph_start_x + graph_end_x)/2), 1005], dire_team, font=rift_team, fill=dire_color, outline_fill=self.colors['black'], outline_width=4)

        composition = self.draw_image_centered(composition, laurels_icon, [laurels_x[0], laurels_y], [40, 40])
        composition = self.draw_image_centered(composition, laurels_icon, [laurels_x[1], laurels_y], [40, 40])

        composition.save(image_path)

    @staticmethod
    def download_opendata_if_necessary(cache_path, match_id):
        # Delete previous image
        json_path = os.path.join(cache_path, 'post_game-{0}.json'.format(match_id))
        if os.path.isfile(json_path):
            with open(json_path, 'r') as json_file:
                json_content = json.loads(json_file.read())
            return json_content

        # Download json to file
        r = requests.get("https://api.opendota.com/api/matches/{0}".format(match_id))
        if r.status_code != 200:
            return None

        json_content = r.json()
        with open(json_path, "w") as json_file:
            json_file.write(json.dumps(json_content))

        return json_content

    def generate_tournament_global(self, tournament_id):
        heroes = db.session.query(DotaHero).all()

        # Delete previous image
        image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'tournament_global-{0}.png'.format(tournament_id))
        if os.path.isfile(image_path): os.remove(image_path)

        # Generate image
        composition = Image.open(
            os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'preti8_teams-background.png')).convert('RGBA')

        image_draw = ImageDraw.Draw(composition)
        rift_title = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 72)
        rift_text = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_regular.otf'), 72)
        rift_subtitle = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 72)
        self.draw_text_outlined_center_align(image_draw, [960, 35], 'The International 8', rift_title, fill=self.colors['ti_green'], outline_fill=self.colors['black'], outline_width=4)

        # Most successful
        successful = []
        successful_stat = []
        for hero_stat in db.session.query(DotaStatTounamentHero)\
                .filter(DotaStatTounamentHero.id_tn==tournament_id, DotaStatTounamentHero.nb_pick!=0)\
                .order_by(desc(DotaStatTounamentHero.mean_is_win))\
                .limit(8)\
                .all():
            hero = next((hero for hero in heroes if hero.id == int(hero_stat.hero_id)), None)
            if hero is not None:
                successful.append(hero)
                successful_stat.append(hero_stat)

        # Side WR
        radian_wr = 49.5
        dire_wr = 50.5

        # Remaining heroes
        not_picked_heroes = []
        for hero_stat in db.session.query(DotaStatTounamentHero).filter(DotaStatTounamentHero.id_tn==tournament_id, DotaStatTounamentHero.nb_pick==0).all():
            hero = next((hero for hero in heroes if hero.id == int(hero_stat.hero_id)), None)
            if hero is not None:
                not_picked_heroes.append(hero)

        # Top Picks & Bans
        picks = []
        picks_stat = []
        bans = []
        bans_stat = []
        for hero_stat in db.session.query(DotaStatTounamentHero).filter(DotaStatTounamentHero.id_tn==tournament_id).order_by(desc(DotaStatTounamentHero.nb_pick)).limit(4).all():
            hero = next((hero for hero in heroes if hero.id == int(hero_stat.hero_id)), None)
            if hero is not None:
                picks.append(hero)
                picks_stat.append(hero_stat)
        for hero_stat in db.session.query(DotaStatTounamentHero).filter(DotaStatTounamentHero.id_tn==tournament_id).order_by(desc(DotaStatTounamentHero.nb_ban)).limit(3).all():
            hero = next((hero for hero in heroes if hero.id == int(hero_stat.hero_id)), None)
            if hero is not None:
                bans.append(hero)
                bans_stat.append(hero_stat)

        # Draw everything

        hero_height = 90
        hero_width = int(256*hero_height/144)
        hero_x = 1350
        hero_y_side_padding = 250
        hero_y_padding = 10
        hero_y_bans_padding = 2*hero_height + 2*hero_y_padding
        successful_x_padding = 500
        hero_y = [{0: hero_y_side_padding,
                  1: hero_y_side_padding + hero_height + hero_y_padding,
                  2: hero_y_side_padding + 2*(hero_height + hero_y_padding),
                  3: hero_y_side_padding + 3*(hero_height + hero_y_padding),
                  4: hero_y_side_padding + 4*(hero_height + hero_y_padding),
                  5: hero_y_side_padding + 5*(hero_height + hero_y_padding),
                  6: hero_y_side_padding + 6*(hero_height + hero_y_padding),
                  7: hero_y_side_padding + 7*(hero_height + hero_y_padding)},
                  {0: hero_y_bans_padding + hero_y_side_padding + 3 * (hero_height + hero_y_padding),
                   1: hero_y_bans_padding + hero_y_side_padding + 4 * (hero_height + hero_y_padding),
                   2: hero_y_bans_padding + hero_y_side_padding + 5 * (hero_height + hero_y_padding)}]
        for i in range(0, len(picks)):
            hero_image = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img',
                                                'hero_rectangle', picks[i].short_name + '.png')).convert('RGBA')
            self.draw_image(composition, hero_image, [hero_x, hero_y[0][i]], [None, hero_height])
        for i in range(0, len(bans)):
            hero_image = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img',
                                                'hero_rectangle', bans[i].short_name + '.png')).convert('RGBA')
            self.draw_image(composition, hero_image, [hero_x, hero_y[1][i]], [None, hero_height])
        for i in range(0, len(successful)):
            hero_image = Image.open(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img',
                                                'hero_rectangle', successful[i].short_name + '.png')).convert('RGBA')
            self.draw_image(composition, hero_image, [hero_x- successful_x_padding, hero_y[0][i]], [None, hero_height])

        image_draw = ImageDraw.Draw(composition)
        for i in range(0, len(picks)):
            image_draw.text([hero_x + hero_width + 20, hero_y[0][i]], '{0} ({1:.1f} %)'.format(picks_stat[i].nb_pick, picks_stat[i].mean_is_win*100), font=rift_text, fill=self.colors['white'])
        for i in range(0, len(bans)):
            image_draw.text([hero_x + hero_width + 20, hero_y[1][i]], '{0} ({1:.1f} %)'.format(bans_stat[i].nb_ban, bans_stat[i].mean_is_win*100), font=rift_text, fill=self.colors['white'])
        self.draw_text_center_align(image_draw, [hero_x + 250, hero_y[0][0] - 100], 'Most Picks', font=rift_subtitle, fill=self.colors['white'])
        self.draw_text_center_align(image_draw, [hero_x + 250, hero_y[1][0] - 100], 'Most Bans', font=rift_subtitle, fill=self.colors['white'])

        self.draw_text_center_align(image_draw, [hero_x + 250 - successful_x_padding, hero_y[0][0] - 100], 'Best Picks', font=rift_subtitle, fill=self.colors['white'])
        for i in range(0, 8):
            image_draw.text([hero_x + hero_width + 20 - successful_x_padding, hero_y[0][i]], '{0:.1f} % ({1})'.format(successful_stat[i].mean_is_win*100, successful_stat[i].nb_pick), font=rift_text, fill=self.colors['white'])
        min_never_picked_x = 50
        max_never_picked_x = 800
        self.draw_text_center_align(image_draw, [425, hero_y[1][0] - 100], 'Never Picked', font=rift_subtitle, fill=self.colors['white'])

        composition.save(image_path)

    def generate_team_faceoff(self, team_id_1, team_id_2):
        # Delete previous image
        image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'team_faceoff-{0}-{1}.png'.format(team_id_1, team_id_2))
        if os.path.isfile(image_path): os.remove(image_path)

        # Generate image
        composition = Image.open(
            os.path.join(os.path.dirname(__file__), '..', 'ressources', 'img', 'preti8_teams-background.png')).convert('RGBA')

        image_draw = ImageDraw.Draw(composition)
        rift_title = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 72)
        image_draw.text([500, 100], '{0}'.format(team_id_1), font=rift_title, fill=self.colors['ti_green'])
        image_draw.text([500, 400], 'VS', font=rift_title, fill=self.colors['ti_green'])
        image_draw.text([500, 700], '{0}'.format(team_id_2), font=rift_title, fill=self.colors['ti_green'])

        composition.save(image_path)

    @staticmethod
    def draw_image(composition, image, position, size):
        new_width = int(image.size[0] * size[1] / image.size[1])
        new_height = size[1]

        resized_image = image.resize([new_width, new_height], Image.LANCZOS)
        composition.paste(resized_image, box=position)

    @staticmethod
    def draw_image_centered(composition, image, position, size):
        new_width = int(image.size[0] * size[1] / image.size[1])
        new_height = size[1]

        resized_image = image.resize([new_width, new_height], Image.LANCZOS)
        in_plate_image = Image.new('RGBA', (composition.size[0], composition.size[1]))
        in_plate_image.paste(resized_image,
                            box=[position[0] - int(resized_image.size[0] / 2),
                                 position[1] - int(resized_image.size[1] / 2)],
                            mask=resized_image)
        return Image.alpha_composite(composition, in_plate_image)

    @staticmethod
    def draw_team_logo(composition, team_id, position, size, alpha):
        team_logo = Image.open(os.path.join(os.path.dirname(__file__),
                                             '..', 'ressources', 'img',
                                            'team_logos',
                                            team_id + '.png')).convert('RGBA')

        new_width = int(team_logo.size[0] * size[1] / team_logo.size[1])
        new_height = size[1]

        team_logo = team_logo.resize([new_width, new_height], Image.LANCZOS)
        in_place_logo = Image.new('RGBA', (composition.size[0], composition.size[1]))
        in_place_logo.paste(team_logo,
                            box=[position[0] - int(team_logo.size[0] / 2),
                                 position[1] - int(team_logo.size[1] / 2)],
                            mask=team_logo)
        in_place_logo = Image.blend(Image.new('RGBA', (composition.size[0], composition.size[1])), in_place_logo, alpha)
        return Image.alpha_composite(composition, in_place_logo)

    @staticmethod
    def draw_minimap_hero(composition, hero, position, size):
        team_logo = Image.open(os.path.join(os.path.dirname(__file__),
                                             '..', 'ressources', 'img',
                                            'hero_minimap',
                                            hero + '.png')).convert('RGBA')

        new_width = int(team_logo.size[0] * size[1] / team_logo.size[1])
        new_height = size[1]

        team_logo = team_logo.resize([new_width, new_height], Image.LANCZOS)
        in_place_logo = Image.new('RGBA', (composition.size[0], composition.size[1]))
        in_place_logo.paste(team_logo,
                            box=[position[0] - int(team_logo.size[0] / 2),
                                 position[1] - int(team_logo.size[1] / 2)],
                            mask=team_logo)
        return Image.alpha_composite(composition, in_place_logo)


    @staticmethod
    def draw_player_portrait(composition, player_id, position, size):
        player_portrait = Image.open(os.path.join(os.path.dirname(__file__),
                                                   '..', 'ressources', 'img',
                                                  'player_portrait',
                                                  player_id + '.png')).convert('RGBA')

        new_width = int(player_portrait.size[0] * size[1] / player_portrait.size[1])
        new_height = size[1]

        player_portrait = player_portrait.resize([new_width, new_height], Image.LANCZOS)
        in_place_portrait = Image.new('RGBA', (composition.size[0], composition.size[1]))
        in_place_portrait.paste(player_portrait,
                                box=[position[0] - int(player_portrait.size[0] / 2),
                                     position[1] - int(player_portrait.size[1] / 2)],
                                mask=player_portrait)
        return Image.alpha_composite(composition, in_place_portrait)

    @staticmethod
    def draw_text_outlined(draw, position, text, font, fill, outline_fill, outline_width):
        draw.text((position[0] - outline_width, position[1] - outline_width), text, font=font, fill=outline_fill)
        draw.text((position[0] + outline_width, position[1] - outline_width), text, font=font, fill=outline_fill)
        draw.text((position[0] - outline_width, position[1] + outline_width), text, font=font, fill=outline_fill)
        draw.text((position[0] + outline_width, position[1] + outline_width), text, font=font, fill=outline_fill)

        draw.text(position, text, font=font, fill=fill)

    @staticmethod
    def draw_text_outlined_center_align(draw, position, text, font, fill, outline_fill, outline_width):
        w, h = draw.textsize(text=text, font=font)
        new_x = position[0] - int(w/2)

        draw.text((new_x - outline_width, position[1] - outline_width), text, font=font, fill=outline_fill)
        draw.text((new_x + outline_width, position[1] - outline_width), text, font=font, fill=outline_fill)
        draw.text((new_x - outline_width, position[1] + outline_width), text, font=font, fill=outline_fill)
        draw.text((new_x + outline_width, position[1] + outline_width), text, font=font, fill=outline_fill)

        draw.text([new_x, position[1]], text, font=font, fill=fill)

    @staticmethod
    def draw_text_center_align(draw, position, text, font, fill):
        w, h = draw.textsize(text=text, font=font)
        new_x = position[0] - int(w/2)
        draw.text([new_x, position[1]], text, font=font, fill=fill)

    @staticmethod
    def draw_text_left_align(draw, position, text, font, fill):
        w, h = draw.textsize(text=text, font=font)
        draw.text([position[0] - w, position[1]], text, font=font, fill=fill)

    @staticmethod
    def draw_alpha_rectangle(composition, positions, fill, alpha):
        in_place_rectangle = Image.new('RGBA', (composition.size[0], composition.size[1]))
        image_draw = ImageDraw.Draw(in_place_rectangle)
        image_draw.rectangle(xy=positions, fill=fill)
        in_place_rectangle = Image.blend(Image.new('RGBA', (composition.size[0], composition.size[1])), in_place_rectangle, alpha)
        return Image.alpha_composite(composition, in_place_rectangle)
