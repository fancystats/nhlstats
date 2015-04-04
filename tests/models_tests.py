"""

Model Tests
-----------

These tests focus on the storage models themselves

"""

import unittest

from peewee import SqliteDatabase

from nhlstats.models import db_proxy, League, Season

db_proxy.initialize(SqliteDatabase(':memory:'))


class TestModelLeague(unittest.TestCase):
    def setUp(self):
        League.create_table()

    def tearDown(self):
        League.drop_table()

    def test_create(self):
        League.create(
            name='National Hockey League',
            abbreviation='NHL'
        )
        self.assertEqual(League.select().count(), 1)
        league = League.select().first()
        self.assertEqual(league.name, 'National Hockey League')
        self.assertEqual(league.abbreviation, 'NHL')


def test_event_elapsed_time_constaint():
    pass


def test_season_types_and_ids():
    """
    Here we ensure that our season types are in
    the right order, as we rely on this to convert
    to the NHLs numeric season type description
    """
    assert(len(Season.SEASON_TYPES) == 3)
    assert(len(Season.get_season_types()) == 3)
    assert(Season.get_season_type_id('preseason') == 1)
    assert(Season.get_season_type_id('regular') == 2)
    assert(Season.get_season_type_id('playoffs') == 3)
