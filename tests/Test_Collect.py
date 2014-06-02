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

    def test_nhlteams(self):
        """
        Test our collection of team info. Note that this could
        break as the NHL changes teams (if Anaheim ceased to
        exist, or adds/subtracts teams) or the URLs to team sites.
        """
        teams = collect.NHLTeams().scrape()

        assert(len(teams) == 30)
        assert(teams['Anaheim Ducks'] == 'http://ducks.nhl.com?navid=nav-teamnav-ana')

    def test_nhlschedule(self):
        """
        Test our collections of a season schedule of games
        """
        rego = collect.NHLSchedule('20132014').scrape()

        # There's an 82 game regular season, let's make sure we have all the games.
        assert(len(rego)/15 == 82)

        #{'season': '20132014', 'time': datetime.time(20, 0), 'start': datetime.date(2014, 3, 16), 'visitor': 'Toronto', 'date': datetime.date(2014, 3, 16), 'home': 'Washington', 'type': 'REG'}
        # Let's find the games on March 16th.  NHL.com says there were 9 games.
        marchSixteenth = [game for game in rego if game['start'] == datetime.date(2014, 3, 16)]
        assert(len(marchSixteenth) == 9)

        # Now just the game between the Caps and the Leafs on that day:
        capsGame = [game for game in marchSixteenth if game['home'] == 'Washington']
        assert(len(capsGame) == 1)

        # Check the start time is correct.  7PM UTC is 3PM EDT
        assert(capsGame[0]['time'] == datetime.time(19, 0))

        # Check to make sure that the right season is set for all games.
        self.assertListEqual([game for game in rego if game['season'] != '20132014'], [])

        playoffs = collect.NHLSchedule('20132014', 'POST').scrape()

        # Check to make sure that the right season is set for all games.
        self.assertListEqual([game for game in playoffs if game['season'] != '20132014'], [])

        # Ensure that Boston-Montreal is the only game listed for May 1st, and that it
        # starts at 11:30 UTC.
        mayFirst = [game for game in playoffs if game['start'] == datetime.date(2014, 5, 1)]
        assert(len(mayFirst) == 1)
        assert(mayFirst[0]['visitor'] == u'Montr\xe9al' and mayFirst[0]['home'] == 'Boston')
        assert(mayFirst[0]['time'] == datetime.time(23, 30))

        # Let's try getting some data from the first post-lockout pre-season
        postLockoutPre = collect.NHLSchedule('20052006', 'PRE').scrape()
        sepTwentySixth = [game for game in postLockoutPre if game['start'] == datetime.date(2005, 9, 26)]
        assert(len(sepTwentySixth) == 1)
        assert(sepTwentySixth[0]['visitor'] == 'Vancouver' and sepTwentySixth[0]['home'] == 'Calgary')
        assert(sepTwentySixth[0]['time'] == datetime.time(1, 0))

        # And one final thing, make sure we can get the first post lockout season and there
        # are 82 games per team.
        postLockout = collect.NHLSchedule('20052006').scrape()
        assert(len(postLockout)/15 == 82)

    def test_nhlgamereports(self):
        """
        Test our ability to grab the game report id
        """
        reports = collect.NHLGameReports('20132014').scrape()

        # First ensure every result has a report id.  We don't want any without.
        # Some games in a season won't have them yet if it's active, but that's
        # expected as they aren't daded until close to the game.
        self.assertListEqual([game for game in reports if not game.get('reportid')], [])

        # Since this is a completed season, however, we expect every game should
        # have one
        assert(len(reports)/15 == 82)

        # Let's grab the March 16th Caps game like we did in the schedule tests
        # and ensure we have the expected report id for it
        capsGame = [game for game in reports if game['start'] == datetime.date(2014, 3, 16) and game['home'] == 'Washington']
        assert(len(capsGame) == 1)
        assert(capsGame[0]['reportid'] == '021014')

        # Now let's grab an older season to make sure it works way back when
        postLockout = collect.NHLGameReports('20052006').scrape()
        assert(len(postLockout)/15 == 82)

        # Let's check the post lockout post season, and ensure we can retrieve
        # a specific game id
        postLockoutPostSeason = collect.NHLGameReports('20052006', 'POST').scrape()
        yeOldePlayoffGame = [game for game in postLockoutPostSeason if game['start'] == datetime.date(2006, 4, 24) and game['home'] == 'Carolina']

        # Make sure we got just one game:
        assert(len(yeOldePlayoffGame) == 1)
        assert(yeOldePlayoffGame[0]['reportid'] == '030122')

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
        assert(events[0]['description'] == 'Period Start- Local time: 3:08 EDT')
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
