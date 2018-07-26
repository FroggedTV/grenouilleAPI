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
        elif key == "ti8_group_a":
            self.generate_csv_ti8_group('a')
        elif key == "ti8_group_b":
            self.generate_csv_ti8_group('b')

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

    def generate_csv_ti8_group(self, group):
        csv_data = db.session.query(CSVData).filter(CSVData.key == 'ti8_group_' + group).one_or_none()
        if csv_data is None: return;

        csv_reader = csv.reader(StringIO(csv_data.value), delimiter=',')
        header = next(csv_reader)
        header = {k: v for v, k in enumerate(header)}
        for row in csv_reader:
            # Delete previous image
            image_path = os.path.join(self.app.config['IMG_GENERATE_PATH'],
                                      'ti8_group_' + group + '.png')
            if os.path.isfile(image_path):
                os.remove(image_path)

            # Generate image
            composition = Image.open(
                os.path.join(os.path.dirname(__file__), 'img_ressources', 'ti8_group-background.png'))
            image_draw = ImageDraw.Draw(composition)
            composition.save(image_path)
