"""

Model Tests
-----------

These tests focus on the storage models themselves

"""

import unittest

from peewee import SqliteDatabase

from nhlstats.models import db_proxy, League, Season, SeasonType

db_proxy.initialize(SqliteDatabase(':memory:'))


class ModelTestCase(unittest.TestCase):
    MODELS = []

    def setUp(self):
        for model in self.MODELS:
            model.create_table()

    def tearDown(self):
        for model in self.MODELS:
            model.drop_table()


class TestModelLeague(ModelTestCase):
    MODELS = [League]

    def test_create(self):
        League.create(
            name='National Hockey League',
            abbreviation='NHL'
        )
        self.assertEqual(League.select().count(), 1)
        league = League.select().first()
        self.assertEqual(league.name, 'National Hockey League')
        self.assertEqual(league.abbreviation, 'NHL')


class TestModelSeasonType(ModelTestCase):
    MODELS = [League, SeasonType]

    def test_create(self):
        league = League.create(
            name='National Hockey League',
            abbreviation='NHL'
        )
        season_type = SeasonType.create(
            league=league,
            name='Regular'
        )
        self.assertEqual(league.season_types.count(), 1)
        self.assertIn(season_type, league.season_types)


class TestModelSeason(ModelTestCase):
    MODELS = [League, SeasonType, Season]

    def test_create(self):
        league = League.create(
            name='National Hockey League',
            abbreviation='NHL'
        )
        season_type = SeasonType.create(
            league=league,
            name='Regular'
        )
        season = season = Season.create(
            league=league,
            year='2014-15',
            type=season_type
        )
        self.assertEqual(league.seasons.count(), 1)
        self.assertIn(season, league.seasons)
