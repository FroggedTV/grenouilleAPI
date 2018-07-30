import logging
import csv
import os
from io import StringIO

from PIL import Image, ImageDraw, ImageColor

from models import db, CSVData

class ImageGenerator:
    """Class helper to generate stats images.

    Attributes:
        app: Flask application.
    """

    def __init__(self, app):
        self.app = app

    def generate_csv_image(self, key):
        """Generate images of a target CSV key.

        Args:
            key: CSV key to generate.
        """
        if key == "preti8_teams":
            self.generate_csv_preti8_teams()
        elif key == "preti8_players":
            self.generate_csv_preti8_players()
        elif key == "ti8_groups":
            self.generate_csv_ti8_groups()

    def generate_csv_preti8_teams(self):
        csv_data = db.session.query(CSVData).filter(CSVData.key=='preti8_teams').one_or_none()
        if csv_data is None: return;

        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}
        for row in csv_reader:
            # Delete previous image
            image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'], 'preti8_teams-' + row[header['teamid']] + '.png')
            if os.path.isfile(image_path):
                os.remove(image_path)

            # Generate image
            composition = Image.open(os.path.join(os.path.dirname(__file__), 'img_ressources', 'preti8_teams-background.png'))
            image_draw = ImageDraw.Draw(composition)
            composition.save(image_path)

    def generate_csv_preti8_players(self):
        csv_data = db.session.query(CSVData).filter(CSVData.key == 'preti8_players').one_or_none()
        if csv_data is None: return;

        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}
        for row in csv_reader:
            # Delete previous image
            image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'],
                                      'preti8_players-' + row[header['playerid']] + '.png')
            if os.path.isfile(image_path):
                os.remove(image_path)

            # Generate image
            composition = Image.open(
                os.path.join(os.path.dirname(__file__), 'img_ressources', 'preti8_players-background.png'))
            image_draw = ImageDraw.Draw(composition)
            composition.save(image_path)

    def generate_csv_ti8_groups(self):
        csv_data = db.session.query(CSVData).filter(CSVData.key == 'ti8_groups').one_or_none()
        if csv_data is None: return;

        # Manage data
        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}

        # Delete previous image
        image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'],
                                  'ti8_groups.png')
        if os.path.isfile(image_path):
            os.remove(image_path)

        # Generate image
        composition = Image.open(os.path.join(os.path.dirname(__file__), 'img_ressources', 'ti8_group-background.png'))
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
            team_logo = Image.open(os.path.join(os.path.dirname(__file__),
                                                'img_ressources',
                                                'team_logos',
                                                row[header['teamid']] + '.png'))
            new_width = int(team_logo.size[0] * logo_height  / team_logo.size[1])
            team_logo = team_logo.resize([new_width, logo_height], Image.LANCZOS)

            if row[header['group']] == 'a':
                current_team_x = group_a_x
                current_team_y = group_a_y
            else:
                current_team_x = group_b_x
                current_team_y = group_b_y

            composition.paste(team_logo,
                              box=[current_team_x + logo_offset_x - int(team_logo.size[0]/2),
                                   current_team_y + logo_offset_y - int(team_logo.size[1]/2)],
                              mask=team_logo)


            if row[header['group']] == 'a':
                group_a_y += team_slot_offset_y
            else:
                group_b_y += team_slot_offset_y




        composition.save(image_path)
