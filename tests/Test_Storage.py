"""
These tests focus on the database storage aspect
"""

import sqlalchemy as sa

from nhlstats import storage


def test_engine():
    """
    Ensure the creation of a simple in memory db engine succeeds.
    """
    container = storage.Container('sqlite:///:memory:')
    assert(isinstance(container.engine, sa.engine.Engine))
