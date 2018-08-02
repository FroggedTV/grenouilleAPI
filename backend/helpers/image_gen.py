import logging
import csv
import os
from io import StringIO

from PIL import Image, ImageDraw, ImageColor, ImageFont

from models import db, CSVData

class ImageGenerator:
    """Class helper to generate stats images.

    Attributes:
        app: Flask application.
    """

    def __init__(self, app):
        self.app = app

    def generate_csv_image(self, key, team_id = None, player_id = None):
        """Generate images of a target CSV key.

        Args:
            key: CSV key to generate.
            team_id: Team ID holder to image generation
            player_id: Player ID holder to image generation
        """
        if key == "preti8_teams":
            self.generate_csv_preti8_teams(team_id)
        elif key == "preti8_players":
            self.generate_csv_preti8_players(player_id)
        elif key == "ti8_groups":
            self.generate_csv_ti8_groups()

    def generate_csv_preti8_teams(self, team_id = None):
        csv_data = db.session.query(CSVData).filter(CSVData.key=='preti8_teams').one_or_none()
        if csv_data is None: return;

        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}
        for row in csv_reader:
            if team_id is not None and team_id != int(row[header['teamid']]):
                continue

            # Delete previous image
            image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'preti8_teams-' + row[header['teamid']] + '.png')
            if os.path.isfile(image_path): os.remove(image_path)

            # Generate image
            composition = Image.open(os.path.join(os.path.dirname(__file__), 'img_ressources', 'preti8_teams-background.png'))
            image_draw = ImageDraw.Draw(composition)

            composition = self.draw_team_logo(composition, row[header['teamid']], [400, 400],  [None, 100])

            composition.save(image_path)

    def generate_csv_preti8_players(self, player_id = None):
        csv_data = db.session.query(CSVData).filter(CSVData.key == 'preti8_players').one_or_none()
        if csv_data is None: return;

        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}
        for row in csv_reader:
            if (len(row[header['playerid']]) == 0 or (not row[header['playerid']].isdigit()) or
                    (player_id is not None and player_id != int(row[header['playerid']]))):
                continue

            # Delete previous image
            image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'preti8_players-' + row[header['playerid']] + '.png')
            if os.path.isfile(image_path): os.remove(image_path)

            # Generate image
            composition = Image.open(os.path.join(os.path.dirname(__file__), 'img_ressources', 'preti8_players-background.png'))
            image_draw = ImageDraw.Draw(composition)
            self.draw_text(image_draw, row[header['team']], [500, 500])
            self.draw_text(image_draw, row[header['pseudo']], [700, 700])
            composition = self.draw_player_portrait(composition, row[header['playerid']], [300, 700], [None, 200])

            composition = self.draw_team_logo(composition, row[header['teamid']], [400, 400],  [None, 100])

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
        composition = Image.open(os.path.join(os.path.dirname(__file__), 'img_ressources', 'ti8_group-background.png')).convert('RGBA')
        image_draw = ImageDraw.Draw(composition)

        # Draw
        group_a_x = 102
        group_b_x = 585
        group_a_y = 214
        group_b_y = 214
        team_slot_offset_y = 55
        logo_height = 40
        logo_offset_x = 75
        logo_offset_y = 25
        for row in csv_reader:
            if row[header['group']] == 'a':
                current_team_x = group_a_x
                current_team_y = group_a_y
            else:
                current_team_x = group_b_x
                current_team_y = group_b_y

            composition = self.draw_team_logo(composition,
                                              row[header['teamid']],
                                              [current_team_x + logo_offset_x, current_team_y + logo_offset_y],
                                              [None, logo_height])

            if row[header['group']] == 'a':
                group_a_y += team_slot_offset_y
            else:
                group_b_y += team_slot_offset_y

        composition.save(image_path)

    @staticmethod
    def draw_team_logo(composition, team_id, position, size):
        team_logo = Image.open(os.path.join(os.path.dirname(__file__),
                                            'img_ressources',
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
        return Image.alpha_composite(composition, in_place_logo)

    @staticmethod
    def draw_text(draw, text, position):
        font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'img_ressources', 'fonts', 'rift', 'fort_foundry_rift_regular.otf'), 64)
        draw.text(position, text, font=font)


    @staticmethod
    def draw_player_portrait(composition, player_id, position, size):
        player_portrait = Image.open(os.path.join(os.path.dirname(__file__),
                                                  'img_ressources',
                                                  'player_portrait',
                                                  player_id + '.png')).convert('RGBA')

        new_width = int(player_portrait.size[0] * size[1] / player_portrait.size[1])
        new_height = size[1]

        team_logo = player_portrait.resize([new_width, new_height], Image.LANCZOS)
        in_place_portrait = Image.new('RGBA', (composition.size[0], composition.size[1]))
        in_place_portrait.paste(player_portrait,
                                box=[position[0] - int(team_logo.size[0] / 2),
                                     position[1] - int(team_logo.size[1] / 2)],
                                mask=player_portrait)
        return Image.alpha_composite(composition, in_place_portrait)
