
import logging

from version import __version__

logger = logging.getLogger(__name__)
logger.debug('Loading %s ver %s' % (__name__, __version__))


# Actions represents the available textual items that can be passed to main
# to drive dispatch. These should be all lower case, no spaces or underscores.
actions = [
    'collect',
    'update',
    'testignore',   # Allows the bin app to be run without calling into here.
]


def GetDataForGame(game):
    pass


def GetDataForGames(games=[]):
    for game in games:
        GetDataForGame(game)


def GetGames(active=True, beginning=None, end=None):
    """
    Return a tuple of games.  Updates gets finished games to check for updated stats,
    if False (default) it returns active games. beginning and end allow you set a range
    for the search, with no end indicating until the time.
    """


def main(action='collect'):
    """
    The main entry point for the application
    """
    logger.debug('Dispatching action %s' % action)
    # By default, we collect info on current games
    if action == 'collect':
        GetDataForGames(GetGames(active=True))
    # Otherwise we can look to update finished games
    elif action == 'update':
        GetDataForGames(GetGames(active=False))
    elif action in actions:
        raise NotImplementedError('Action "%s" is known, but not (yet?) implemented' % action)
    else:
        raise ValueError('Unknown action "%s"' % action)
