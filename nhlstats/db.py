import os

from playhouse.db_url import connect

from nhlstats import models
from nhlstats.models import db_proxy

# FIXME: We should probably put all the database connection code in one place
# instead of having equivalent code in api and nhlstats both.


def connect_db():
    global db
    db = connect(os.environ.get('DATABASE_URL') or 'sqlite:///default.db')
    db_proxy.initialize(db)


def create_tables():
    for model in models.MODELS:
        m = getattr(models, model)
        if m.table_exists():
            print('{} table already exists, skipping...'.format(model))
            continue
        print('Creating {} table...'.format(model))
        m.create_table()


def drop_tables():
    for model in reversed(models.MODELS):
        m = getattr(models, model)
        if not m.table_exists():
            print('{} does not exist, skipping...'.format(model))
            continue
        print('Dropping {} table...'.format(model))
        m.drop_table()
