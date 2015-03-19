# Just a placeholder for now...

class Config(object):
    DATABASE = {
        'name': 'nhlstats.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'shhhh'
