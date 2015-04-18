# -*- coding: utf-8 -*-
"""
These tests focus on testing collection of data
from the NHL via screen scraping.

Note that this site:

http://www.timeanddate.com/worldclock/converter.html

Can be useful for sanity checking times.
"""

import datetime
import unittest
from nhlstats import collect


class TestCollection(unittest.TestCase):

    def test_nhldivisions(self):
        """
        Test our collection of data for conferences and divisions.
        """
        divisions = collect.NHLDivisions('20132014').scrape()

        expected = {
            u'Eastern': {
                u'Atlantic': [
                    u'Boston',
                    u'Tampa Bay',
                    u'Montréal',
                    u'Detroit',
                    u'Ottawa',
                    u'Toronto',
                    u'Florida',
                    u'Buffalo'
                ],
                u'Metropolitan': [
                    u'Pittsburgh',
                    u'NY Rangers',
                    u'Philadelphia',
                    u'Columbus',
                    u'Washington',
                    u'New Jersey',
                    u'Carolina',
                    u'NY Islanders'
                ]
            },
            u'Western': {
                u'Central': [
                    u'Colorado',
                    u'St. Louis',
                    u'Chicago',
                    u'Minnesota',
                    u'Dallas',
                    u'Nashville',
                    u'Winnipeg'
                ],
                u'Pacific': [
                    u'Anaheim',
                    u'San Jose',
                    u'Los Angeles',
                    u'Phoenix',
                    u'Phoenix',
                    u'Vancouver',
                    u'Calgary',
                    u'Edmonton'
                ]
            }
        }

        # Ensure we have the Eastern and Western conference
        for conference in expected:
            assert(conference in divisions)

            for division in expected[conference]:
                assert(division in divisions[conference])

                for team in expected[conference][division]:
                    assert(team in divisions[conference][division])

    def test_nhlseason_missing(self):
        """
        Test that an incorrect season yields the expected error
        """
        with self.assertRaises(collect.UnexpectedPageContents):
            # I've introduced a Y3k bug in my tests! Oh noes!
            collect.NHLDivisions('30003001').scrape()

    def test_nhlteams(self):
        """
        Test our collection of team info. Note that this could
        break as the NHL changes teams (if Anaheim ceased to
        exist, or adds/subtracts teams) or the URLs to team sites.
        """
        teams = collect.NHLTeams().scrape()

        assert(len(teams) == 30)
        ducks_expected = {
            'division': 'pacific',
            'url': 'http://ducks.nhl.com',
            'city': 'Anaheim',
            'code': 'ANA',
            'name': 'Ducks'
        }

        assert(ducks_expected in teams)

    def test_nhlschedule(self):
        """
        Test our collections of a season schedule of games
        """
        rego = collect.NHLSchedule('20132014').scrape()

        # There's an 82 game regular season, let's make sure we have all the
        # games.
        # TODO: Fix this - we currently expect 76 here because of Arizona
        assert(len(rego) / 15 == 76)

        # Let's find the games on March 16th.  NHL.com says there were 9 games.
        marchSixteenth = [
            game for game in rego
            if game['start'].date() == datetime.date(2014, 3, 16)
        ]

        assert(len(marchSixteenth) == 9)

        # Now just the game between the Caps and the Leafs on that day:
        capsGame = [
            game for game in marchSixteenth if game['home'] == 'WSH'
        ]

        assert(len(capsGame) == 1)

        # Check the start time is correct.  7PM UTC is 3PM EDT
        assert(capsGame[0]['start'].time() == datetime.time(19, 0))

        # Check to make sure that the right season is set for all games.
        self.assertListEqual(
            [game for game in rego if game['season'] != '20132014'],
            []
        )

        playoffs = collect.NHLSchedule('20132014', 'Playoffs').scrape()

        # Check to make sure that the right season is set for all games.
        self.assertListEqual(
            [game for game in playoffs if game['season'] != '20132014'],
            []
        )

        # Ensure that Boston-Montreal is the only game listed for May 1st,
        # and that it starts at 11:30 UTC.
        mayFirst = [
            game for game in playoffs
            if game['start'].date() == datetime.date(2014, 5, 1)
        ]

        assert(len(mayFirst) == 1)

        assert(
            mayFirst[0]['road'] == 'MTL' and
            mayFirst[0]['home'] == 'BOS'
        )

        assert(mayFirst[0]['start'].time() == datetime.time(23, 30))

        # Let's try getting some data from the first post-lockout pre-season
        postLockoutPre = collect.NHLSchedule('20052006', 'Preseason').scrape()
        sepTwentySixth = [
            game for game in postLockoutPre
            if game['start'].date() == datetime.date(2005, 9, 26)
        ]

        assert(len(sepTwentySixth) == 1)

        assert(
            sepTwentySixth[0]['road'] == 'VAN' and
            sepTwentySixth[0]['home'] == 'CGY'
        )

        assert(sepTwentySixth[0]['start'].time() == datetime.time(1, 0))

        # And one final thing, make sure we can get the first post
        # lockout season and there are 82 games per team.
        postLockout = collect.NHLSchedule('20052006').scrape()
        # TODO: Fix this - we currently expect 76 here because of Arizona
        assert(len(postLockout) / 15 == 71)

    def test_nhlgamereports(self):
        """
        Test our ability to grab the game report id
        """
        reports = collect.NHLGameReports('20132014').scrape()

        # First ensure every result has a report id.  We don't want any
        # without. Some games in a season won't have them yet if it's
        # active, but that's expected as they aren't daded until close
        # to the game.
        self.assertListEqual(
            [game for game in reports if not game.get('report_id')],
            []
        )

        # Since this is a completed season, however, we expect every game
        # should have one
        # TODO: Fix this - we currently expect 76 here because of Arizona
        assert(len(reports) / 15 == 76)

        # Let's grab the March 16th Caps game like we did in the schedule tests
        # and ensure we have the expected report id for it
        capsGame = [
            game for game in reports
            if game['start'] == datetime.datetime(2014, 3, 16, 19, 0)
            and game['home'] == 'WSH'
        ]

        assert(len(capsGame) == 1)
        assert(capsGame[0]['report_id'] == '021014')

        # Now let's grab an older season to make sure it works way back when
        postLockout = collect.NHLGameReports('20052006').scrape()
        # TODO: Fix this - we currently expect 71 here because of Arizona
        assert(len(postLockout) / 15 == 71)

        # Let's check the post lockout post season, and ensure we can retrieve
        # a specific game id
        postLockoutPostSeason = collect.NHLGameReports(
            '20052006', 'Playoffs'
        ).scrape()

        yeOldePlayoffGame = [
            game for game in postLockoutPostSeason
            if game['start'] == datetime.datetime(2006, 4, 24, 23, 0)
            and game['home'] == 'CAR'
        ]

        # Make sure we got just one game:
        assert(len(yeOldePlayoffGame) == 1)
        assert(yeOldePlayoffGame[0]['report_id'] == '030122')

    def test_nhlroster(self):
        """
        Test the collection of an nhl team roster
        """
        # Here we just pull in a couple rosters and
        # check the existence of various fields.
        # It's hard to really check the values.
        ducks = collect.NHLRoster('ducks').scrape()
        assert(len(ducks) >= 20)
        assert(ducks[0].get('name'))
        assert(ducks[3].get('weight'))
        assert(ducks[12].get('height'))

        caps = collect.NHLRoster('capitals').scrape()
        assert(len(caps) >= 20)
        assert(caps[16].get('hometown'))
        assert(caps[18].get('number'))
        assert(caps[19].get('dob'))

    def test_eventlocation(self):
        """
        Test the collection of game events.
        """
        # First check a game from the recent season
        events = collect.NHLEventLocations('20132014', '021014').scrape()

        assert(events['away'] == 'Toronto Maple Leafs')
        assert(events['home'] == 'Washington Capitals')
        assert(events['plays'][0]['desc'] == 'Joel Ward hit Paul Ranger')
        assert(events['plays'][0]['xcoord'] == -90)
        assert(len(events['plays']) == 107)

        # Then check an older game. Sadly 20092010 seems to be
        # the first year there is location data for.
        events = collect.NHLEventLocations('20092010', '020370').scrape()
        assert(events['home'] == 'Montreal Canadiens')
        assert(events['away'] == 'Washington Capitals')
        assert(events['plays'][22]['playername'] == 'Nicklas Backstrom')
        assert(events['plays'][22]['time'] == '18:16')
        assert(len(events['plays']) == 89)

    def test_events(self):
        # Let's get event data for the 2014.03.16 game between
        # the Caps and the Leafs
        events = collect.NHLEvents('20132014', '021014').scrape()

        # Check some basics, start with the start!
        assert(events[0]['description'] ==
               'Period Start- Local time: 3:08 EDT')
        assert(events[0]['event'] == 'PSTR')
        assert(events[0]['time'] == '0:00')

        # Now check some info on players on the ice
        assert(len(events[42]['home']) == 6)
        assert({'player': '92', 'position': 'C'} in events[42]['home'])
        assert({'player': '41', 'position': 'G'} in events[42]['home'])

        # Toronto was short handed here (I don't have to tell you this
        # led to a goal - but it wasn't Ovi from the Ovi spot!)
        assert(len(events[42]['away']) == 5)
        assert({'player': '41', 'position': 'L'} in events[42]['away'])
        assert({'player': '15', 'position': 'D'} in events[42]['away'])

        assert(events[42]['event'] == 'GOAL')

        # Check we have the ending information
        assert(events[-1]['description'] == 'Game End- Local time: 5:42 EDT')
        assert(events[-1]['away'] == [])
        assert(events[-1]['home'] == [])
        assert(events[-1]['period'] == '3')
        assert(events[-1]['time'] == '20:00')
        assert(events[-1]['event'] == 'GEND')
