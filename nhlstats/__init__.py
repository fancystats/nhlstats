
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


def GetGames(updates=False):
    """
    Return a tuple of games.  Updates gets finished games to check for updated stats,
    if False (default) it returns active games.
    """
    if updates:
        # Get a list of recently finished games to check for updates on
        pass
    else:
        # Get a list of active games.
        pass


def main(action):
    """
    The main entry point for the application
    """
    GetDataForGames(GetGames(action))
