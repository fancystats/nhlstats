
import logging

from version import __version__

from .db import create_tables, drop_tables
from .models import League, Season, Team, Conference, Division, Arena
from .collect import NHLSchedule, NHLTeams, NHLDivisions, NHLArena


logger = logging.getLogger(__name__)
logger.debug('Loading {} ver {}'.format(__name__, __version__))


# Actions represents the available textual items that can be passed to main
# to drive dispatch. These should be all lower case, no spaces or underscores.
actions = [
    'collect',
    'update',
    'populate',
    'syncdb',
    'dropdb',
    'testignore',   # Allows the bin app to be run without calling into here.
]

# This represents seasons we officially support. Should eventually be
# supported by external configuration of seasons to collect
seasons = [
    '20132014'
]


def get_data_for_game(game):
    pass


def get_data_for_games(games=[]):
    for game in games:
        get_data_for_game(game)


def get_games(active=True, beginning=None, end=None):
    """
    Return a tuple of games.  Updates gets finished games to check for updated stats,
    if False (default) it returns active games. beginning and end allow you set a range
    for the search, with no end indicating until the time.
    """


def populate():
    """
    Retrieves base information including
    teams, rosters, seasons, arenas, etc.
    """
    # In the event they don't exist, create the tables.
    create_tables()
    # This is NHL stats, after all, let's start by creating the NHL
    league = League.get_or_create(name='NHL')

    # Get the latest set of division information
    divisions = NHLDivisions().scrape()
    for conference in divisions:
        con_model = Conference.get_or_create(league=league, name=conference)
        for division in divisions[conference]:
            Division.get_or_create(conference=con_model, name=division)

    for team in NHLTeams().scrape():
        # Convert the textual divison name to a Division model
        team['division'] = Division.get(Division.name ** team['division'])
        Team.get_or_create(**team)
        Arena.get_or_create(**NHLArena(team['acronym']).scrape())

    # Gather our seasons:
    for years in seasons:
        divisions = NHLDivisions(years).scrape()
        for season_type, season_type_str in Season.SEASON_TYPES:
            Season.get_or_create(league=league, year=years, type=season_type)

            for game in NHLSchedule(years, season_type).scrape():
                pass


def main(action='collect'):
    """
    The main entry point for the application
    """
    logger.debug('Dispatching action {}'.format(action))
    # By default, we collect info on current games
    if action == 'collect':
        get_data_for_games(get_games(active=True))
    # Otherwise we can look to update finished games
    elif action == 'update':
        get_data_for_games(get_games(active=False))
    elif action == 'populate':
        populate()
    elif action == 'syncdb':
        create_tables()
    elif action == 'dropdb':
        drop_tables()
    elif action in actions:
        raise NotImplementedError('Action "{}" is known, but not (yet?) implemented'.format(action))
    else:
        raise ValueError('Unknown action "{}"'.format(action))
