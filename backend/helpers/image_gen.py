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
            composition = Image.open(os.path.join(os.path.dirname(__file__), 'img_ressources', 'preti8_teams-background.png')).convert('RGBA')

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
                                              logo_array[row[header['teamid']]]['size'])
            image_draw = ImageDraw.Draw(composition)

            rift_bold_title = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'img_ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 150)
            rift_bold_sub = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'img_ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 58)
            green = ImageColor.getrgb('#83a94c')
            black = ImageColor.getrgb('#000000')
            white = ImageColor.getrgb('#ffffff')
            self.draw_text_outlined(image_draw, [85, 51], row[header['team']], font=rift_bold_title, fill=green, outline_fill=black, outline_width=5)

            row_1_x = 800
            row_1_y = 350
            row_1_line = 65
            row_1_inc = 225
            row_2_x = row_1_x + 40
            row_2_y = 330
            row_2_inc = 225
            row_3_x = 1400
            row_4_x = row_3_x + 40
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y], 'Classement', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_line], 'DPC', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_inc], 'DPC', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_inc + row_1_line], 'Obtenus', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + 2*row_1_inc], 'Nombre', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + 2*row_1_inc + row_1_line], 'De games', rift_bold_sub, white)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y-5], row[header['classement_dpc']], font=rift_bold_title, fill=green,
                                    outline_fill=black, outline_width=5)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y + row_2_inc-5], row[header['total_dpc']], font=rift_bold_title, fill=green,
                                    outline_fill=black, outline_width=5)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y + 2*row_2_inc-5], row[header['nombre_games']], font=rift_bold_title, fill=green,
                                    outline_fill=black, outline_width=5)

            self.draw_text_left_align(image_draw, [row_3_x, row_1_y], 'Winrate', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_3_x, row_1_y + row_1_line], '4 mois -', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_3_x, row_1_y + row_1_inc], 'Gains', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_3_x, row_1_y + row_1_inc + row_1_line], 'saison -', rift_bold_sub, white)
            self.draw_text_outlined(image_draw, [row_4_x, row_2_y-5], row[header['wr']] + ' %', font=rift_bold_title, fill=green,
                                    outline_fill=black, outline_width=5)
            self.draw_text_outlined(image_draw, [row_4_x, row_2_y + row_2_inc-5], '$ ' + row[header['gains']], font=rift_bold_title, fill=green,
                                    outline_fill=black, outline_width=5)

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
            composition = Image.open(os.path.join(os.path.dirname(__file__), 'img_ressources', 'preti8_players-background.png')).convert('RGBA')
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
                                              logo_array[row[header['teamid']]]['size'])
            image_draw = ImageDraw.Draw(composition)

            rift_bold_title = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'img_ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 150)
            rift_bold_sub = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'img_ressources', 'fonts', 'rift', 'fort_foundry_rift_bold.otf'), 58)
            green = ImageColor.getrgb('#83a94c')
            black = ImageColor.getrgb('#000000')
            white = ImageColor.getrgb('#ffffff')

            self.draw_text_outlined(image_draw, [85, 51], row[header['pseudo']], font=rift_bold_title, fill=green, outline_fill=black, outline_width=5)
            image_draw.text([85, 215], row[header['team']], font=rift_bold_sub, fill=white)

            row_1_x = 950
            row_1_y = 350
            row_1_line = 65
            row_1_inc = 225
            row_2_x = row_1_x + 40
            row_2_y = 330
            row_2_inc = 225
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y], 'Héro du', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_line], 'Moment', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_inc], 'Networth', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + row_1_inc + row_1_line], 'Moyen', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + 2*row_1_inc], 'Nombre de', rift_bold_sub, white)
            self.draw_text_left_align(image_draw, [row_1_x, row_1_y + 2*row_1_inc + row_1_line], 'héros joués', rift_bold_sub, white)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y-5], row[header['hero_privilegie']].replace('_', ' '), font=rift_bold_title, fill=green,
                                    outline_fill=black, outline_width=5)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y + row_2_inc-5], row[header['networth']], font=rift_bold_title, fill=green,
                                    outline_fill=black, outline_width=5)
            self.draw_text_outlined(image_draw, [row_2_x, row_2_y + 2*row_2_inc-5], row[header['nombre_heros']], font=rift_bold_title, fill=green,
                                    outline_fill=black, outline_width=5)

            composition = self.draw_minimap_hero(composition, row[header['hero_privilegie']], [1450, 130], [None, 150])
            composition = self.draw_minimap_hero(composition, row[header['hero_signature_1']], [1600, 130], [None, 150])
            composition = self.draw_minimap_hero(composition, row[header['hero_signature_2']], [1750, 130], [None, 150])

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
        in_place_logo = Image.blend(Image.new('RGBA', (composition.size[0], composition.size[1])), in_place_logo, 0.7)
        return Image.alpha_composite(composition, in_place_logo)

    @staticmethod
    def draw_minimap_hero(composition, hero, position, size):
        team_logo = Image.open(os.path.join(os.path.dirname(__file__),
                                            'img_ressources',
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

    @staticmethod
    def draw_text_outlined(draw, position, text, font, fill, outline_fill, outline_width):
        draw.text((position[0] - outline_width, position[1] - outline_width), text, font=font, fill=outline_fill)
        draw.text((position[0] + outline_width, position[1] - outline_width), text, font=font, fill=outline_fill)
        draw.text((position[0] - outline_width, position[1] + outline_width), text, font=font, fill=outline_fill)
        draw.text((position[0] + outline_width, position[1] + outline_width), text, font=font, fill=outline_fill)

        draw.text(position, text, font=font, fill=fill)

    @staticmethod
    def draw_text_left_align(draw, position, text, font, fill):
        w, h = draw.textsize(text=text, font=font)
        draw.text([position[0] - w, position[1]], text, font=font, fill=fill)
