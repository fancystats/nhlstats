#!/usr/bin/env python

from flask.ext.script import Manager

from nhlstats import db
from nhlstats.app import app

manager = Manager(app)


@manager.command
def create_tables():
    db.create_tables()


@manager.command
def drop_tables():
    db.drop_tables()


if __name__ == "__main__":
    manager.run()