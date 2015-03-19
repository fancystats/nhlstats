"""
Models creates a series of relevant Peewee models

Ex: Game events
http://www.nhl.com/scores/htmlreports/20132014/PL021195.HTM
"""

from peewee import CharField, DateField, DateTimeField, ForeignKeyField, \
    IntegerField, TextField

from nhlstats.db import BaseModel


class Arena(BaseModel):
    name = CharField()
    location = CharField()
    capacity = IntegerField()

    class Meta:
        db_table = 'arenas'

    def __unicode__(self):
        return self.name


class League(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'leagues'

    def __unicode__(self):
        return self.name


class Season(BaseModel):
    league = ForeignKeyField(League)
    name = CharField()

    class Meta:
        db_table = 'seasons'

    def __unicode__(self):
        return self.name


class Conference(BaseModel):
    league = ForeignKeyField(League)
    name = CharField()

    class Meta:
        db_table = 'leagues'

    def __unicode__(self):
        return self.name


class Division(BaseModel):

    conference = ForeignKeyField(Conference)
    name = CharField()

    class Meta:
        db_table = 'conferences'

    def __unicode__(self):
        return self.name


class Team(BaseModel):
    city = CharField()

    name = CharField()
    acronym = CharField()
    division = ForeignKeyField(Division)

    class Meta:
        db_table = 'teams'
        order_by = ('city', 'name')

    def __unicode__(self):
        return '{} {}'.format(self.city, self.name)


class Player(BaseModel):
    SHOOTS = [('L', 'Left'),
              ('R', 'Right')]

    TEAM_STATUSES = [('pro', 'Pro'),
                     ('farm', 'Farm'),
                     ('prospect', 'Prospect'),
                     ('retired', 'Retired')]

    external_id = IntegerField(unique=True)
    team = ForeignKeyField(Team, related_name='players')
    name = CharField()
    no = IntegerField()
    pos = CharField()
    shoots = CharField(choices=SHOOTS, verbose_name='Shoots/Catches')
    dob = DateField(verbose_name='Date of Birth')
    pob = CharField(verbose_name='Place of Birth')
    height = IntegerField()
    weight = IntegerField()
    salary = IntegerField(null=True)
    seasons = IntegerField(default=0)
    drafted = CharField()
    signed = CharField()
    assets = TextField()
    flaws = TextField()
    potential = CharField()
    status = CharField()
    team_status = CharField(choices=TEAM_STATUSES)

    class Meta:
        db_table = 'players'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class Coach(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'coaches'

        def __unicode__(self):
            return self.name


class Game(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    season = ForeignKeyField(Season)
    arena = ForeignKeyField(Arena)
    attendence = IntegerField()
    home_team = ForeignKeyField(Team)
    away_team = ForeignKeyField(Team)
    reportid = CharField()
    game_type = CharField(choices=('PRE', 'REG', 'POST'))


class Event(BaseModel):
    game = ForeignKeyField(Game)
    period = IntegerField()
    strength = CharField(choices=('EV', 'PP', 'SH'))
    elapsed_time = IntegerField()
    description = CharField()
    home_offensive_line = CharField()
    home_defensive_line = CharField()
    home_goalie = ForeignKeyField(Player)
    away_offensive_line = CharField()
    away_defensive_line = CharField()
    away_goalie = ForeignKeyField(Player)


class PlayerEvent(BaseModel):
    player = ForeignKeyField(Player)
    event = ForeignKeyField(Event)
    team = ForeignKeyField(Team)
    position = CharField(choices=('L', 'C', 'R', 'LD', 'RD', 'G', 'E'))
