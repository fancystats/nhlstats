
import logging

logger = logging.getLogger(__name__)


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
    else:
        # Get a list of active games.


def main(updates=False):
    """
    The main entry point for the application
    """
    GetDataForGames(GetGames(updates))
