"""

Model Tests
-----------

These tests focus on the storage models themselves

"""

import unittest

from peewee import SqliteDatabase

from nhlstats import models

models.db_proxy.initialize(SqliteDatabase(':memory:'))


def test_event_elapsed_time_constaint():
    pass


def test_season_types_and_ids():
    """
    Here we ensure that our season types are in
    the right order, as we rely on this to convert
    to the NHLs numeric season type description
    """
    assert(len(models.Season.SEASON_TYPES) == 3)
    assert(len(models.Season.get_season_types()) == 3)
    assert(models.Season.get_season_type_id('preseason') == 1)
    assert(models.Season.get_season_type_id('regular') == 2)
    assert(models.Season.get_season_type_id('playoffs') == 3)
