from flask_peewee.db import Database

from nhlstats.app import app

db = Database(app)


def create_tables():
    from nhlstats import models
    for model in models.MODELS:
        m = getattr(models, model)
        if m.table_exists():
            print('{} table already exists, skipping...'.format(model))
            continue
        print('Creating {} table...'.format(model))
        m.create_table()


def drop_tables():
    from nhlstats import models
    for model in reversed(models.MODELS):
        m = getattr(models, model)
        if not m.table_exists():
            print('{} does not exist, skipping...'.format(model))
            continue
        print('Dropping {} table...'.format(model))
        m.drop_table()
