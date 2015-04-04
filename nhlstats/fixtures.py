"""

Fixtures
--------

An easy way to load and unload data from the database.

"""

import logging
import os

from playhouse.dataset import DataSet

from nhlstats.db import DEFAULT_SQLITE_DB

FIXTURES_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'fixtures'))

logger = logging.getLogger(__name__)


def connect_dataset():
    """Returns a DataSet connection to the database."""
    return DataSet(os.environ.get('DATABASE_URL') or DEFAULT_SQLITE_DB)


def freeze(basedir=None, format='json'):
    """Dump the data stored in the database into a series of fixtures."""
    ds = connect_dataset()
    logger.info('Freezing the database into fixtures...')
    if not basedir:
        basedir = FIXTURES_DIR
    logger.info('Using {} as the fixtures directory...'.format(basedir))
    if not os.path.isdir(basedir):
        logger.warn('{} directory does not exist, creating...'.format(basedir))
        os.makedirs(basedir)
    for name in ds.tables:
        table = ds[name]
        filename = os.path.join(basedir, '{}.{}'.format(name, format))
        logger.info('Freezing fixture for {} in {}...'.format(name, filename))
        ds.freeze(table.all(), format=format, filename=filename)


def thaw(basedir=None):
    """Load data from a series of fixtures into the database."""

    ds = connect_dataset()
    logger.info('Thawing data from fixtures and loading into database...')
    if not basedir:
        basedir = FIXTURES_DIR
    if not os.path.isdir(basedir):
        logger.error('{} directory does not exist, exiting...'.format(basedir))
        return
    fixtures = os.listdir(basedir)
    logger.debug('Found {} fixtures in {}...'.format(len(fixtures), basedir))
    for fixture in fixtures:
        if os.path.isfile(fixture):
            filename = fixture.split('/')[-1]
            table, format = filename.split('.')[-1]
            if format not in ['json', 'csv']:
                logger.warn('Unrecognized format {}, skipping...'.format(
                    format))
                continue
            if table not in ds:
                logger.warn('Table {} does not exist, skipping...'.format(
                    table))
                continue
            table = ds[table]
            logger.info('Thawing {} into {} table...'.format(fixture, table))
            table.thaw(format=format, filename=filename, strict=True)
