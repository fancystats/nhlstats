#!/usr/bin/env python

from flask.ext.script import Manager

from nhlstats.app import app
from nhlstats.db import create_tables, drop_tables

manager = Manager(app)


@manager.command
def syncdb():
    create_tables()


@manager.command
def dropdb():
    drop_tables()


if __name__ == "__main__":
    manager.run()