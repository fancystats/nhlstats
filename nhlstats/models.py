# -*- coding: utf-8 -*-
"""

Models
======

 Creates a series of relevant Peewee models.

Ex: Game events
http://www.nhl.com/scores/htmlreports/20132014/PL021195.HTM
"""

import logging

from .version import __version__

from peewee import BooleanField, CharField, DateField, DateTimeField, \
    ForeignKeyField, IntegerField, TextField, Model, Proxy

logger = logging.getLogger(__name__)
logger.debug('Loading {} ver {}'.format(__name__, __version__))


# Order should be the order these tables are created.
MODELS = [
    'Arena',
    'League',
    'SeasonType',
    'Season',
    'Conference',
    'Division',
    'Team',
    'Schedule',
    'Player',
    'PlayerSkaterStat',
    'PlayerGoalieStat',
    'Roster',
    'Coach',
    'Game',
    'Lineup',
    'Event',
    'EventPlayer'
]

db_proxy = Proxy()


class BaseModel(Model):

    class Meta:
        database = db_proxy


class Arena(BaseModel):

    """
    Represents a venue in which a game is played.
    """
    name = CharField()
    street = CharField()
    city = CharField()
    state = CharField()
    country = CharField()
    postal_code = CharField()
    # TODO: find out how we can get capacity data
    capacity = IntegerField(null=True)

    class Meta:
        db_table = 'arenas'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class League(BaseModel):
    name = CharField()
    abbreviation = CharField()

    class Meta:
        db_table = 'leagues'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class SeasonType(BaseModel):

    """
    Represents a season type within a league. Such as preseason, regular or
    playoffs. These are in relation to a league because each league can have
    arbitrarty identifiers `external_id` for each season type.
    """
    league = ForeignKeyField(League, related_name='season_types')
    name = CharField()
    external_id = CharField(null=True)

    class Meta:
        db_table = 'season_types'

    def __unicode__(self):
        return self.name


class Season(BaseModel):
    league = ForeignKeyField(League, related_name='seasons',
                             on_delete='CASCADE', on_update='CASCADE')
    year = CharField()
    type = ForeignKeyField(SeasonType, related_name='seasons')

    class Meta:
        db_table = 'seasons'
        order_by = ('league', 'year')
        indexes = (
            # create a unique on league/year/type
            (('league', 'year', 'type'), True),
        )

        def __unicode__(self):
            return self.year


class Conference(BaseModel):
    league = ForeignKeyField(League, related_name='conferences',
                             on_delete='CASCADE', on_update='CASCADE')
    name = CharField(unique=True)

    class Meta:
        db_table = 'conferences'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class Division(BaseModel):
    conference = ForeignKeyField(Conference, related_name='divisions',
                                 on_delete='CASCADE', on_update='CASCADE')
    name = CharField(unique=True)

    class Meta:
        db_table = 'divisions'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class Team(BaseModel):
    division = ForeignKeyField(Division, related_name='teams')
    city = CharField()
    name = CharField()
    code = CharField()
    url = CharField()

    class Meta:
        db_table = 'teams'
        order_by = ('city', 'name')

    def __unicode__(self):
        return '{} {}'.format(self.city, self.name)


class Schedule(BaseModel):
    season = ForeignKeyField(Season, related_name='scheduled_games',
                             on_delete='CASCADE', on_update='CASCADE')
    day = IntegerField()
    game = IntegerField()
    date = DateField()
    home = ForeignKeyField(Team, related_name='scheduled_home_games',
                           on_delete='CASCADE', on_update='CASCADE')
    road = ForeignKeyField(Team, related_name='scheduled_road_games',
                           on_delete='CASCADE', on_update='CASCADE')

    class Meta:
        db_table = 'schedules'
        order_by = ['season', 'game']

    def __unicode__(self):
        return '{} {} Day {} Game {}'.format(self.league.name,
                                             self.type,
                                             self.day,
                                             self.game)


class Player(BaseModel):
    SHOOTS = [('L', 'Left'),
              ('R', 'Right')]

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

    @property
    def height_imperial(self):
        if self.height:
            return '{}\'{}"'.format(self.height / 12, self.height % 12)
        return 'N/A'

    @property
    def height_metric(self):
        if self.height:
            return '{}cm'.format(round(self.height * 2.54))
        return 'N/A'

    @property
    def weight_imperial(self):
        if self.weight:
            return '{}lbs'.format(self.weight)
        return 'N/A'

    @property
    def weight_metric(self):
        if self.weight:
            return '{}kg'.format(round(self.weight * 0.453592))
        return 'N/A'


class PlayerSkaterStat(BaseModel):
    player = ForeignKeyField(Player, related_name='skater_stats')
    season = ForeignKeyField(Season, related_name='skater_stats')
    team = ForeignKeyField(Team, related_name='skater_stats')
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


class Roster(BaseModel):

    """
    Represents a team's roster for a specific season. The relationship between
    a team and a player.
    """
    season = ForeignKeyField(Season, related_name='roster')
    team = ForeignKeyField(Team, related_name='roster')
    player = ForeignKeyField(Player, related_name='rosters')
    no = IntegerField()

    class Meta:
        db_table = 'rosters'


class Coach(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'coaches'
        order_by = ('name',)

        def __unicode__(self):
            return self.name


class Game(BaseModel):
    season = ForeignKeyField(Season, related_name='games')
    arena = ForeignKeyField(Arena, related_name='games', null=True)
    attendence = IntegerField(null=True)
    home = ForeignKeyField(Team, related_name='home_games')
    road = ForeignKeyField(Team, related_name='road_games')
    report_id = CharField(null=True)
    start = DateTimeField()
    end = DateTimeField(null=True)

    class Meta:
        db_table = 'games'
        order_by = ('start',)


class Lineup(BaseModel):

    """
    Represents a team's lineup for a specific game. Should probably include
    scratched players.
    """
    game = ForeignKeyField(Game)
    team = ForeignKeyField(Team)
    Player = ForeignKeyField(Player)
    scratched = BooleanField(default=False)

    class Meta:
        db_table = 'lineups'


class Event(BaseModel):

    """
    Represents an event that occured within a game.

    :param game: Game in which event occured.
    : type game: Game
    :param team: Team responsible for event.
    :type team: Team
    :param number: Number associated with event.
    :type number: integer
    :param period: Period in which the event occured.
    :type period: integer
    :param strength: Strength the current team had during event.
    :type strength: string
    :param elapse: Amount of time elapsed in period (in seconds).
    :type elapsed: integer
    :param remaining: Amount of time remaining in period (in seconds).
    :type remaining: integer
    :param type: The type of event that occured.
    :type type: string
    :param zone: The zone in which the event occured.
    :type zone: string or None
    :param description: A description of the event.
    :type description: string or None
    :param player1: Primary player involved in event (ex. goal scorer).
    :type player1: Player or None
    :param player2: Secondary player involved in event (ex. primary assist).
    :type player2: Player or None
    :param player3: Third player involved in an event (ex. secondary assist).
    :type player3: Player or None
    :param shot_type: The type of shot taken (if any).
    :type shot_type: string or None
    :param distance: Distance from opponents net.
    :type distance: integer or None
    :param penalty: Type of penalty taken (if any).
    :type penalty: string or None
    :param penalty_minutes: Amount of penalty minutes given for penalty.
    :type penalty_minutes: integer or None
    """
    STRENGTHS = [('ev', 'Even Strength'),
                 ('pp', 'Power Play'),
                 ('sh', 'Short Handed')]
    EVENT_TYPES = [('block', 'Blocked Shot'),
                   ('end', 'End of Period'),
                   ('face', 'Faceoff'),
                   ('give', 'Giveaway'),
                   ('goal', 'Goal'),
                   ('hit', 'Hit'),
                   ('miss', 'Missed Shot'),
                   ('penalty', 'Penalty'),
                   ('shot', 'Shot on Net'),
                   ('start', 'Start of Period'),
                   ('stop', 'Stoppage'),
                   ('take', 'Takewaway')]
    ZONES = [('home', 'Home'),
             ('neutral', 'Neutral'),
             ('road', 'Road')]
    SHOT_TYPES = [('slap', 'Slap Shot'),
                  ('snap', 'Snap Shot'),
                  ('wrist', 'Wrist Shot')]

    game = ForeignKeyField(Game, related_name='events')
    team = ForeignKeyField(Team, null=True)
    number = IntegerField(verbose_name='#')
    period = IntegerField()
    strength = CharField(choices=STRENGTHS, default='EV')
    elapsed = IntegerField()
    remaining = IntegerField()
    type = CharField(choices=EVENT_TYPES)
    zone = CharField(choices=ZONES, null=True)
    description = CharField(null=True)
    player1 = ForeignKeyField(Player, null=True, related_name='player1_events')
    player2 = ForeignKeyField(Player, null=True, related_name='player2_events')
    player3 = ForeignKeyField(Player, null=True, related_name='player3_events')
    shot_type = CharField(choices=SHOT_TYPES, null=True)
    distance = IntegerField(null=True)
    penalty = CharField(null=True)
    penalty_minutes = IntegerField(null=True)

    class Meta:
        db_table = 'events'
        order_by = ('game', 'number')


class EventPlayer(BaseModel):

    """
    Represents a player who was on the ice at the time of the event.

    :param event: Event in which the player was on the ice.
    :type event: Event
    :param team: The team the player was playing for (denormalization?).
    :type team: Team
    :param Player: The player on the ice during the event.
    :type player: Player
    """
    event = ForeignKeyField(Event, related_name='players')
    team = ForeignKeyField(Team)
    player = ForeignKeyField(Player)

    class Meta:
        db_table = 'event_players'
