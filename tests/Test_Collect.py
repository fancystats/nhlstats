"""
These tests focus on testing collection of data
from the NHL via screen scraping
"""

from nhlstats import collect


def test_teams():
    """
    Test our collection of team data
    """
    teams = collect.NHLSeason('20132014')
    assert(len(teams.scrape()) == 30)
