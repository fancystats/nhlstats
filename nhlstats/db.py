import logging
import os

from playhouse.db_url import connect

from nhlstats import models
from nhlstats.models import db_proxy
from nhlstats.version import __version__


logger = logging.getLogger(__name__)
logger.debug('Loading {} ver {}'.format(__name__, __version__))


DEFAULT_SQLITE_DB = 'sqlite:///nhlstats.db'


# FIXME: We should probably put all the database connection code in one place
# instead of having equivalent code in api and nhlstats both.


def connect_db():
    db_url = os.environ.get('DATABASE_URL') or DEFAULT_SQLITE_DB
    db_proxy.initialize(connect(db_url))

    if db_url == DEFAULT_SQLITE_DB:
        logger.warn('Using default SQLite database.')


def create_tables():
    connect_db()
    for model in models.MODELS:
        m = getattr(models, model)
        if m.table_exists():
            logger.debug('{} table already exists, skipping...'.format(model))
            continue
        logger.info('Creating {} table...'.format(model))
        m.create_table()


def drop_tables():
    connect_db()
    for model in reversed(models.MODELS):
        m = getattr(models, model)
        if not m.table_exists():
            logger.debug('{} does not exist, skipping...'.format(model))
            continue
        logger.info('Dropping {} table...'.format(model))
        m.drop_table()
