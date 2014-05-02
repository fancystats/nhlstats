# -*- coding: utf-8 -*-
"""
These tests focus on testing collection of data
from the NHL via screen scraping
"""

import unittest
from nhlstats import collect


class TestCollection(unittest.TestCase):
    def test_nhlseason(self):
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

    def test_nhlseason_missing(self):
        """
        Test that an incorrect season yields the expected error
        """
        with self.assertRaises(collect.UnexpectedPageContents):
            # I've introduced a Y3k bug in my tests! Oh noes!
            collect.NHLSeason('30003001').scrape()

    def test_teams(self):
        """
        Test our collection of team info. Note that this could
        break as the NHL changes teams (if Anaheim ceased to
        exist, or adds/subtracts teams) or the URLs to team sites.
        """
        teams = collect.Teams().scrape()

        assert(len(teams) == 30)
        assert(teams['Anaheim Ducks'] == 'http://ducks.nhl.com?navid=nav-teamnav-ana')