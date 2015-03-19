from flask_peewee.db import Database

from nhlstats.app import app

db = Database(app)


class BaseModel(db.Model):
    pass
