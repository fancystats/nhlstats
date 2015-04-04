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
