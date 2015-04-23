import sys
import re
import time
import urllib2
import logging
import datetime

from version import __version__

from .db import create_tables, drop_tables, connect_db
from .models import League, Season, SeasonType, Team, Conference, \
                    Division, Arena, Game
from .collect import NHLTeams, NHLDivisions, NHLArena, NHLGameReports, \
                     NHLEvents


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
    'shell',
    'testignore',   # Allows the bin app to be run without calling into here.
]


# TODO: Proper exception handling and clean up
# TODO: retry at least once on IncompleteRead
# TODO: Handle timezones.
# TODO: Allow for multiple levels of verbosity, squelch db stuff in debug
# TODO: Add ability to specify current time via CLI/env
# TODO: Add ability to specify wait timer when grabbing new pages via CLI/env
# TODO: Add ability to specify seasons to collect via CLI/env
# TODO: Make logging a pass through by default in the library itself.
# TODO: Do a unicode/str audit
seasons = [
    '20142015'
]


def get_data_for_game(game, use_cache=False):
    events = NHLEvents(game.season.year, game.report_id, use_cache=use_cache)

    for event in events.scrape():
        if event['event'] == 'GEND':
            # TODO: Inevitably there are some bugs here - we don't consider
            # what happens when a game runs past midnight or somehow starts
            # early in the AM - but this lets us test basic stuff
            time_match = re.match(
                'Game End\- Local time\: '
                '(?P<hour>[0-9]{1,2})\:(?P<minute>[0-9]{2}) '
                '(?P<timezone>[A-Z]{3})',
                event['description']
            )

            if time_match:
                try:
                    game.end = datetime.datetime.strptime(
                        '{}-{:02d}-{:02d} {:02d}:{}'.format(
                            game.start.year,
                            int(game.start.month),
                            int(game.start.day),
                            int(time_match.group('hour')),
                            time_match.group('minute'),
                        ),
                        '%Y-%m-%d %I:%M'
                    )
                except ValueError:
                    # TODO: DO NOT CHECK THIS IN!!!!!!
                    game.end = datetime.datetime(2000, 01, 01, 1, 1, 1)
                game.save()
                logger.info('Game {} has ended at {}'.format(
                    game, game.end
                ))
            else:
                raise ValueError('Unable to parse GEND')

    if not events.loaded_from_cache:
        logger.warning('Waiting to download to be polite.')
        time.sleep(5)


def get_data_for_games(games, use_cache=False):
    if games is None:
        games = []

    success_counter = 0
    failure_counter = 0

    for game in games:
        try:
            get_data_for_game(game, use_cache)
            success_counter += 1
        except urllib2.HTTPError:
            logger.warning(
                'Unable to retrieve game report for {}'.format(game)
            )
            failure_counter += 1
        except:
            logger.exception('Error getting data for {}'.format(game))
            sys.exit(1)

    logger.info('Processed {} games'.format(success_counter))
    logger.info('Failed to process {} games'.format(failure_counter))


def populate(use_cache):
    """
    Retrieves base information including
    teams, rosters, seasons, arenas, etc.
    """
    # In the event they don't exist, create the tables.
    create_tables()

    # This is NHL stats, after all, let's start by creating the NHL
    league = League.get_or_create(
        name='National Hockey League',
        abbreviation='NHL'
    )

    # Add season types
    SeasonType.get_or_create(league=league, name='Preseason', external_id='1')
    SeasonType.get_or_create(league=league, name='Regular', external_id='2')
    SeasonType.get_or_create(league=league, name='Playoffs', external_id='3')

    # Get the latest set of division information
    divisions = NHLDivisions(use_cache=use_cache).scrape()
    for conference in divisions:
        con_model = Conference.get_or_create(league=league, name=conference)
        for division in divisions[conference]:
            Division.get_or_create(conference=con_model, name=division)

    for team in NHLTeams(use_cache=use_cache).scrape():
        # Convert the textual divison name to a Division model
        team['division'] = Division.get(Division.name ** team['division'])
        Team.get_or_create(**team)
        Arena.get_or_create(
            **NHLArena(team['code'], use_cache=use_cache).scrape()
        )

    # Gather our seasons:
    for years in seasons:
        divisions = NHLDivisions(years, use_cache=use_cache).scrape()

        for season_type in SeasonType.select():
            season = Season.get_or_create(
                league=league,
                year=years,
                type=season_type
            )

            games = NHLGameReports(
                years,
                season_type.name,
                use_cache=use_cache
            ).scrape()

            for game in games:
                game['home'] = Team.get(code=game['home'])
                game['road'] = Team.get(code=game['road'])
                game['season'] = season
                Game.get_or_create(**game).save()


def main(action='collect', use_cache=False):
    """
    The main entry point for the application
    """
    logger.debug('Dispatching action {}'.format(action))
    # By default, we collect info on current games
    if action == 'collect':
        connect_db()
        get_data_for_games(
            Game.get_active_games(),
            use_cache
        )
    # Otherwise we can look to update finished games
    elif action == 'update':
        connect_db()
        get_data_for_games(
            Game.get_orphaned_games(),
            use_cache
        )
        get_data_for_games(
            Game.get_games_in_date_range(),
            use_cache
        )
    elif action == 'populate':
        populate(use_cache)
    elif action == 'syncdb':
        create_tables()
    elif action == 'dropdb':
        drop_tables()
    elif action == 'shell':
        connect_db()
        # Ghetto ass shell command!
        # TODO: Get a more respectable shell
        import pdb; pdb.set_trace()
    elif action in actions:
        raise NotImplementedError(
            'Action "{}" is known, but not (yet?) implemented'.format(action))
    else:
        raise ValueError('Unknown action "{}"'.format(action))
