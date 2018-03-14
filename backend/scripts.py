from datetime import datetime

from flask_script import Manager

from app import create_app
from models import db, Game, GameVIP, GameVIPType

app = create_app()
manager = Manager(app)


###########
# Scripts #
###########


@manager.command
def insert_all_vips():
    """Upsert all VIP (admins and caster) for the FroggedTV league season 2."""
    db.session().query(GameVIP).delete()
    db.session().commit()
    users = [
        [76561198051212435, GameVIPType.ADMIN, 'Xavier'],
        [76561198211842660, GameVIPType.ADMIN, 'Llewela'],
        [76561198098675996, GameVIPType.ADMIN, 'Autowash'],
        [76561198014066928, GameVIPType.ADMIN, 'Mexx'],
        [76561198038914414, GameVIPType.ADMIN, 'NkZ_'],
        [76561197968638037, GameVIPType.ADMIN, 'DetaX'],
        [76561197990849508, GameVIPType.ADMIN, 'Nark!'],
        [76561197978959964, GameVIPType.ADMIN, 'Nark!2'],
        [76561198072527807, GameVIPType.ADMIN, 'MLC'],
        [76561197961298382, GameVIPType.ADMIN, 'Philaeux'],
        [76561197993366373, GameVIPType.CASTER, 'Luciqno'],
        [76561198009684017, GameVIPType.CASTER, 'v0ja'],
        [76561198017952409, GameVIPType.CASTER, 'Hugo'],
        [76561198131038874, GameVIPType.CASTER, 'YouYou'],
        [76561198277308914, GameVIPType.CASTER, 'Namax'],
        [76561198047244470, GameVIPType.CASTER, 'Bartsake'],
        [76561198078547785, GameVIPType.CASTER, 'Key_'],
        [76561198150315161, GameVIPType.CASTER, 'Apoc'],
        [76561198007225076, GameVIPType.CASTER, 'Profchen'],
        [76561198021075598, GameVIPType.CASTER, 'Celhest'],
        [76561198030827104, GameVIPType.CASTER, 'Kinroi'],
        [76561198280010661, GameVIPType.CASTER, 'InDotaWeTrust'],
        [76561197984501634, GameVIPType.CASTER, 'Neogarfield'],
        [76561198047142880, GameVIPType.CASTER, 'Magic'],
        [76561198045162287, GameVIPType.CASTER, 'Roxa'],
        [76561198073845741, GameVIPType.CASTER, 'PoneySGuito'],
        [76561197966937903, GameVIPType.CASTER, 'Kaeinie'],
        [76561198047949626, GameVIPType.CASTER, 'Kleber'],
        [76561198078233972, GameVIPType.CASTER, 'Manorot20'],
        [76561198062806656, GameVIPType.CASTER, 'BoomEsport1'],
        [76561197979979281, GameVIPType.CASTER, 'BoomEsport2'],
        [76561198347635223, GameVIPType.CASTER, 'SoteyOS'],
        [76561198094493830, GameVIPType.CASTER, 'Whyll'],
        [76561198079970517, GameVIPType.CASTER, 'Yugnatt']
    ]
    for user in users:
        GameVIP.upsert(user[0], user[1], user[2])

@manager.command
def clean_game_database():
    """Clean all matches from database. BE CAREFULL WITH DIS !!!"""
    db.session().query(Game).delete()
    db.session().commit()

#######################
# Setup Manage Script #
#######################
if __name__ == '__main__':
    manager.run()
