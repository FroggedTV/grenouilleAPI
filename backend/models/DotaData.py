from database import db

class DotaHero(db.Model):
    """Dota heroes"""
    __tablename__= 'dota_heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    short_name = db.Column(db.Text(), nullable=False)
    localized_name = db.Column(db.Text(), nullable=False)

    def __init__(self, id, name, short_name, localized_name):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.localized_name = localized_name

    @staticmethod
    def upsert(id, name, short_name, localized_name):
        hero = db.session.query(DotaHero).filter(DotaHero.id==id).one_or_none()
        if hero is None:
            hero = DotaHero(id, name, short_name, localized_name)
            db.session.add(hero)
        hero.id = id
        hero.name = name
        hero.short_name = short_name
        hero.localized_name = localized_name
        db.session.commit()

class DotaItem(db.Model):
    """Dota items"""
    __tablename__= 'dota_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    short_name = db.Column(db.Text(), nullable=False)
    localized_name = db.Column(db.Text(), nullable=False)

    def __init__(self, id, name, short_name, localized_name):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.localized_name = localized_name

    @staticmethod
    def upsert(id, name, short_name, localized_name):
        item = db.session.query(DotaItem).filter(DotaItem.id==id).one_or_none()
        if item is None:
            item = DotaItem(id, name, short_name, localized_name)
            db.session.add(item)
        item.id = id
        item.name = name
        item.short_name = short_name
        item.localized_name = localized_name
        db.session.commit()

class DotaProPlayer(db.Model):
    """Dota pro players"""
    __tablename__= 'dota_pro_players'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    nickname = db.Column(db.Text(), nullable=False)
    team = db.Column(db.BigInteger(), nullable=False)

    def __init__(self, id, name, nickname, team):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.team = team

    @staticmethod
    def upsert(id, name, nickname, team):
        player = db.session.query(DotaProPlayer).filter(DotaProPlayer.id==id).one_or_none()
        if player is None:
            player = DotaProPlayer(id, name, nickname, team)
            db.session.add(player)
        player.id = id
        player.name = name
        player.nickname = nickname
        player.team = team
        db.session.commit()

class DotaProTeam(db.Model):
    """Dota pro players"""
    __tablename__= 'dota_pro_teams'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def upsert(id, name):
        team = db.session.query(DotaProTeam).filter(DotaProTeam.id==id).one_or_none()
        if team is None:
            team = DotaProTeam(id, name)
            db.session.add(team)
        team.id = id
        team.name = name
        db.session.commit()

class DotaStatTounamentHero(db.Model):
    """Tournament stats of a specific hero"""
    __tablename__ = 'stat_tn_hero'
    __bind_key__ = 'stats'

    hero_id = db.Column(db.Numeric(), primary_key=True)
    id_tn = db.Column(db.Numeric(), primary_key=True)
    nb_pick = db.Column(db.Numeric())
    nb_ban = db.Column(db.Numeric())
    nb_match = db.Column(db.Numeric())
    mean_is_win = db.Column(db.Numeric())


class DotaStatTounamentTeamHero(db.Model):
    """Tournament stats of a specific team and heroes"""
    __tablename__ = 'stat_tn_team_hero'
    __bind_key__ = 'stats'

    hero_id = db.Column(db.Numeric(), primary_key=True)
    id_tn = db.Column(db.Numeric(), primary_key=True)
    team_id = db.Column(db.Numeric(), primary_key=True)

    nb_pick = db.Column(db.Numeric())
    nb_ban = db.Column(db.Numeric())
    nb_ban_against = db.Column(db.Numeric())
    nb_match = db.Column(db.Numeric())
    mean_is_win = db.Column(db.Numeric())


class DotaStatTounamentTeam(db.Model):
    """Tournament stats of a specific team and heroes"""
    __tablename__ = 'stat_tn_team'
    __bind_key__ = 'stats'

    tn_id = db.Column(db.Numeric(), primary_key=True)
    team_id = db.Column(db.Numeric(), primary_key=True)

    nb_match = db.Column(db.Numeric())
    mean_is_radiant = db.Column(db.Numeric())
    mean_is_radiant_win = db.Column(db.Numeric())
    mean_is_dire_win = db.Column(db.Numeric())
    mean_is_win = db.Column(db.Numeric())
    mean_is_firstpick = db.Column(db.Numeric())
    mean_duration = db.Column(db.Numeric())
    win_duration = db.Column(db.Numeric())
    lose_duration = db.Column(db.Numeric())
    mean_pct_bounty = db.Column(db.Numeric())


class DotaStatTournament(db.Model):
    """Tournament stats of a specific hero"""
    __tablename__ = 'stat_tn_tn'
    __bind_key__ = 'stats'

    id_tn = db.Column(db.Numeric(), primary_key=True)
    nb_match = db.Column(db.Numeric())
    mean_radiant_win = db.Column(db.Numeric())
    mean_duration = db.Column(db.Numeric())
