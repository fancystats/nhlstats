from flask_peewee.db import Database

from nhlstats.app import app

db = Database(app)


def create_tables():
    from nhlstats import models
    for model in models.MODELS:
        print('Creating {} table...'.format(model))
        model = getattr(models, model)
        model.create_table()


def drop_tables():
    from nhlstats import models
    for model in reversed(models.MODELS):
        print('Dropping {} table...'.format(model))
        model = getattr(models, model)
        model.drop_table(fail_silently=True)
