"""
Models
======

 Creates a series of relevant Peewee models.

Ex: Game events
http://www.nhl.com/scores/htmlreports/20132014/PL021195.HTM
"""

from peewee import CharField, DateField, DateTimeField, ForeignKeyField, \
    IntegerField, TextField

from nhlstats.db import db

# Order should be the order these tables are created.
MODELS = [
    'Arena',
    'League',
    'Season',
    'Conference',
    'Division',
    'Team',
    'Player',
    'Coach',
    'Game',
    'Event',
    'PlayerEvent'
]


class BaseModel(db.Model):
    pass


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
    league = ForeignKeyField(League, related_name='seasons')
    name = CharField()

    class Meta:
        db_table = 'conferences'

    def __unicode__(self):
        return self.name


class Division(BaseModel):
    conference = ForeignKeyField(Conference, related_name='divisions')
    name = CharField()

    class Meta:
        db_table = 'divisions'

    def __unicode__(self):
        return self.name


class Team(BaseModel):
    city = CharField()
    name = CharField()
    acronym = CharField()
    division = ForeignKeyField(Division, related_name='teams')

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
    season = ForeignKeyField(Season, related_name='games')
    arena = ForeignKeyField(Arena, related_name='games')
    attendence = IntegerField()
    home_team = ForeignKeyField(Team, related_name='home_games')
    away_team = ForeignKeyField(Team, related_name='away_games')
    reportid = CharField()
    game_type = CharField(choices=('PRE', 'REG', 'POST'))

    class Meta:
        db_table = 'games'


class Event(BaseModel):
    game = ForeignKeyField(Game, related_name='events')
    period = IntegerField()
    strength = CharField(choices=('EV', 'PP', 'SH'))
    elapsed_time = IntegerField()
    description = CharField()
    home_offensive_line = CharField()
    home_defensive_line = CharField()
    home_goalie = ForeignKeyField(Player, related_name='home_goalie_events')
    away_offensive_line = CharField()
    away_defensive_line = CharField()
    away_goalie = ForeignKeyField(Player, related_name='away_goalie_events')

    class Meta:
        db_table = 'events'


class PlayerEvent(BaseModel):
    player = ForeignKeyField(Player, related_name='player_events')
    event = ForeignKeyField(Event, related_name='player_events')
    team = ForeignKeyField(Team, related_name='player_events')
    position = CharField(choices=('L', 'C', 'R', 'LD', 'RD', 'G', 'E'))

    class Meta:
        db_table = 'player_events'
