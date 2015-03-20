import os

from playhouse.db_url import connect

from nhlstats.models import db_proxy, MODELS

# Will want to move this to a factory at some point.
db = connect(os.environ.get('DATABASE_URL') or 'sqlite:///default.db')
db_proxy.initialize(db)


def create_tables():
    for model in MODELS:
        m = getattr(models, model)
        if m.table_exists():
            print('{} table already exists, skipping...'.format(model))
            continue
        print('Creating {} table...'.format(model))
        m.create_table()


def drop_tables():
    from nhlstats import models
    for model in reversed(MODELS):
        m = getattr(models, model)
        if not m.table_exists():
            print('{} does not exist, skipping...'.format(model))
            continue
        print('Dropping {} table...'.format(model))
        m.drop_table()
