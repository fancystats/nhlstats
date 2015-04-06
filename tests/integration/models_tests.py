"""

Model Integration Tests
=======================

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
        for model in reversed(self.MODELS):
            model.drop_table()

    def create_league(self, **kwargs):
        defaults = {'name': 'National Hockey League', 'abbreviation': 'NHL'}
        defaults.update(kwargs)
        return League.create(**defaults)

    def create_season_type(self, **kwargs):
        defaults = {'name': 'Regular'}
        defaults.update(kwargs)
        return SeasonType.create(**defaults)

    def create_season(self, **kwargs):
        defaults = {'year': '2014-15'}
        defaults.update(kwargs)
        return Season.create(**defaults)


class TestModelLeague(ModelTestCase):
    MODELS = [League]

    def test_create(self):
        self.assertEqual(League.select().count(), 0)
        league = self.create_league()
        self.assertEqual(League.select().count(), 1)
        league = League.select().first()
        self.assertEqual(league.name, 'National Hockey League')
        self.assertEqual(league.abbreviation, 'NHL')


class TestModelSeasonType(ModelTestCase):
    MODELS = [League, SeasonType]

    def test_create(self):
        league = self.create_league()
        season_type = self.create_season_type(league=league)
        self.assertEqual(league.season_types.count(), 1)
        self.assertIn(season_type, league.season_types)


class TestModelSeason(ModelTestCase):
    MODELS = [League, SeasonType, Season]

    def test_create(self):
        league = self.create_league()
        season_type = self.create_season_type(league=league)
        season = self.create_season(league=league, type=season_type)
        self.assertEqual(league.seasons.count(), 1)
        self.assertIn(season, league.seasons)
