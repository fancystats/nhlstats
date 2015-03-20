"""
Models
======

 Creates a series of relevant Peewee models.

Ex: Game events
http://www.nhl.com/scores/htmlreports/20132014/PL021195.HTM
"""

from peewee import CharField, DateField, DateTimeField, ForeignKeyField, \
    IntegerField, TextField, Model, Proxy

# Order should be the order these tables are created.
MODELS = [
    'Arena',
    'League',
    'Season',
    'Conference',
    'Division',
    'Team',
    'Schedule',
    'Player',
    'PlayerSkaterStat',
    'PlayerGoalieStat',
    'Coach',
    'Game',
    'Event',
    'PlayerEvent'
]

db_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class Arena(BaseModel):
    name = CharField()
    location = CharField()
    capacity = IntegerField()

    class Meta:
        db_table = 'arenas'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class League(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'leagues'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class Season(BaseModel):
    SEASON_TYPES = [('preseason', 'Preseason'),
                    ('regular', 'Regular'),
                    ('playoffs', 'Playoffs')]

    league = ForeignKeyField(League, related_name='seasons')
    year = CharField()
    type = CharField(choices=SEASON_TYPES)

    class Meta:
        db_table = 'seasons'
        order_by = ('league', 'year')

    def __unicode__(self):
        return self.year


class Conference(BaseModel):
    league = ForeignKeyField(League, related_name='conferences')
    name = CharField()

    class Meta:
        db_table = 'conferences'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class Division(BaseModel):
    conference = ForeignKeyField(Conference, related_name='divisions')
    name = CharField()

    class Meta:
        db_table = 'divisions'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class Team(BaseModel):
    division = ForeignKeyField(Division, related_name='teams')
    city = CharField()
    name = CharField()
    acronym = CharField()

    class Meta:
        db_table = 'teams'
        order_by = ('city', 'name')

    def __unicode__(self):
        return '{} {}'.format(self.city, self.name)


class Schedule(BaseModel):
    SCHEDULE_TYPES = [('regular', 'Regular'),
                      ('preseason', 'Preseason')]

    league = ForeignKeyField(League, related_name='schedules')
    type = CharField(choices=SCHEDULE_TYPES)
    day = IntegerField()
    game = IntegerField()
    date = DateField()
    home = ForeignKeyField(Team, related_name='home_scheduled_games')
    away = ForeignKeyField(Team, related_name='away_scheduled_games')

    class Meta:
        db_table = 'schedules'
        order_by = ['league', 'type', 'game']

    def __unicode__(self):
        return '{} {} Day {} Game {}'.format(self.league.name,
                                             self.type,
                                             self.day,
                                             self.game)


class Player(BaseModel):
    SHOOTS = [('L', 'Left'),
              ('R', 'Right')]

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
    drafted = CharField(null=True)
    signed = CharField(null=True)
    assets = TextField(null=True)
    flaws = TextField(null=True)
    potential = CharField(null=True)
    status = CharField()

    class Meta:
        db_table = 'players'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class PlayerSkaterStat(BaseModel):
    player = ForeignKeyField(Player, related_name='skater_stats')
    season = ForeignKeyField(Season, related_name='skater_stats')
    team = ForeignKeyField(Team, related_name='skater_stats')
    league = ForeignKeyField(League, related_name='skater_stats')
    gp = IntegerField(null=True, verbose_name='GP')
    g = IntegerField(null=True)
    a = IntegerField(null=True)
    pts = IntegerField(null=True, verbose_name='PTS')
    pm = IntegerField(null=True, verbose_name='+/-')
    pim = IntegerField(null=True, verbose_name='PIM')
    ppg = IntegerField(null=True, verbose_name='PPG')
    shg = IntegerField(null=True, verbose_name='SHG')
    gwg = IntegerField(null=True, verbose_name='GWG')
    shots = IntegerField(null=True)

    class Meta:
        db_table = 'player_skater_stats'
        order_by = ('season', 'team', 'pts')

    def __unicode__(self):
        return '{} {} ({})'.format(self.season,
                                   self.team,
                                   self.league)

    @property
    def ptspgp(self):
        if self.gp and self.pts:
            return '%.2f' % float(self.gp) / self.pts
        return None

    @property
    def shotpct(self):
        if self.shots and self.g:
            return '%.3f' % float(self.shots) / self.g
        return None


class PlayerGoalieStat(BaseModel):
    player = ForeignKeyField(Player, related_name='goalie_stats')
    season = ForeignKeyField(Season, related_name='goalie_stats')
    team = ForeignKeyField(Team, related_name='goalie_stats')
    league = ForeignKeyField(League, related_name='goalie_stats')
    gpi = IntegerField(null=True, verbose_name='GPI')
    w = IntegerField(null=True)
    l = IntegerField(null=True)
    t = IntegerField(null=True)
    otl = IntegerField(null=True, verbose_name='OTL')
    min = IntegerField(null=True)
    so = IntegerField(null=True, verbose_name='SO')
    ga = IntegerField(null=True, verbose_name='GA')
    sha = IntegerField(null=True, verbose_name='SHA')

    class Meta:
        db_table = 'player_goalie_stats'
        order_by = ('-season', 'team', 'gpi')

    def __unicode__(self):
        return '{} {} ({})'.format(self.season, self.team, self.league)

    @property
    def gaa(self):
        if self.ga and self.min:
            return '%.2f' % self.ga / (self.min / 60.0)
        return None

    @property
    def svpct(self):
        if self.ga and self.sha:
            return '%.3f' % (1 - self.ga / float(self.sha))
        return None


class Coach(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'coaches'
        order_by = ('name',)

        def __unicode__(self):
            return self.name


class Game(BaseModel):
    GAME_TYPES = (('PRE', 'Preseason'),
                  ('REG', 'Regular'),
                  ('POST', 'Postseason'))

    start_time = DateTimeField()
    end_time = DateTimeField()
    season = ForeignKeyField(Season, related_name='games')
    arena = ForeignKeyField(Arena, related_name='games')
    attendence = IntegerField()
    home_team = ForeignKeyField(Team, related_name='home_games')
    away_team = ForeignKeyField(Team, related_name='away_games')
    reportid = CharField()
    game_type = CharField(choices=GAME_TYPES)

    class Meta:
        db_table = 'games'
        order_by = ('start_time',)


class Event(BaseModel):
    STRENGTHS = (('EV', 'Even Strength'),
                 ('PP', 'Powerplay'),
                 ('SH', 'Shorthanded'))

    game = ForeignKeyField(Game, related_name='events')
    period = IntegerField()
    strength = CharField(choices=STRENGTHS)
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
    POSITIONS = ('L', 'C', 'R', 'LD', 'RD', 'G', 'E')

    player = ForeignKeyField(Player, related_name='player_events')
    event = ForeignKeyField(Event, related_name='player_events')
    team = ForeignKeyField(Team, related_name='player_events')
    position = CharField(choices=POSITIONS)

    class Meta:
        db_table = 'player_events'
