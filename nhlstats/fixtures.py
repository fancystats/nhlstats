"""

Fixtures
--------

An easy way to load and unload data from the database.

"""

import os

from playhouse.dataset import DataSet
from nhlstats.db import DEFAULT_SQLITE_DB

FIXTURES_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'fixtures'))

db = DataSet(os.environ.get('DATABASE_URL') or DEFAULT_SQLITE_DB)

def freeze(basedir=None, format='json'):
    """Dump the data stored in the database into a series of fixtures."""
    if not basedir:
        basedir = FIXTURES_DIR
    if not os.path.isdir(basedir):
        os.makedirs(basedir)
    for name in db.tables:
        table = db[name]
        filename = os.path.join(basedir, '{}.{}'.format(name, format))
        db.freeze(table.all(), format=format, filename=filename)


def thaw(basedir=None):
    """Load data from a series of fixtures into the database."""
    if not basedir:
        basedir = FIXTURES_DIR
    fixtures = os.listdir(basedir)
    for fixture in fixtures:
        if os.path.isfile(fixture):
            filename = fixture.split('/')[-1]
            table, format = filename.split('.')[-1]
            if format not in ['json', 'csv']:
                continue
            if table not in db:
                continue
            table = db[table]
            table.thaw(format=format, filename=filename, strict=True)
