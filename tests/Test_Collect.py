# -*- coding: utf-8 -*-
"""
These tests focus on testing collection of data
from the NHL via screen scraping
"""

from nhlstats import collect


def test_nhlseason():
    """
    Test our collection of data for a season.
    """
    season = collect.NHLSeason('20132014').scrape()

    expected = {
        'Eastern': {
            'Atlantic': ['Boston', 'Tampa Bay', u'Montréal', 'Detroit', 'Ottawa', 'Toronto', 'Florida', 'Buffalo'],
            'Metropolitan': ['Pittsburgh', 'NY Rangers', 'Philadelphia', 'Columbus', 'Washington', 'New Jersey', 'Carolina', 'NY Islanders']
        },
        'Western': {
            'Central': ['Colorado', 'St. Louis', 'Chicago', 'Minnesota', 'Dallas', 'Nashville', 'Winnipeg'],
            'Pacific': ['Anaheim', 'San Jose', 'Los Angeles', 'Phoenix', 'Phoenix', 'Vancouver', 'Calgary', 'Edmonton']
        }
    }

    # Ensure we have the Eastern and Western conference
    for conference in expected:
        assert(conference in season)

        for division in expected[conference]:
            assert(division in season[conference])

            for team in expected[conference][division]:
                assert(team in season[conference][division])


def test_teams():
    """
    Test our collection of team info
    """
    teams = collect.Teams().scrape()
    assert(len(teams) == 30)
