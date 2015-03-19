from flask import Flask

app = Flask(__name__)
app.config.from_object('nhlstats.config.Config')
app.config.from_envvar('NHLSTATS_SETTINGS', silent=True)
