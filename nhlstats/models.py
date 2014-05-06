"""
Models creates a series of relevant declarative sqlalchemy models

Ex: Game events
http://www.nhl.com/scores/htmlreports/20132014/PL021195.HTM
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, DateTime, CheckConstraint
Base = declarative_base()


class Arenas(Base):
    __tablename__ = 'arenas'

    arena_id = Column(Integer, primary_key=True)

    location = Column(String)
    name = Column(String)
    capacity = Column(Integer)


class People(Base):
    __tablename__ = 'people'

    person_id = Column(Integer, primary_key=True)
    person_name = Column(String)


class Players(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.person_id'))
    season_id = Column(Integer, ForeignKey('seasons.season_id'))
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    number = Column(Integer)


class Coaches(Base):
    __tablename__ = 'coaches'

    coach_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.person_id'))


class Leagues(Base):
    __tablename__ = 'leagues'

    league_id = Column(Integer, primary_key=True)
    name = Column(String)


class Conferences(Base):
    __tablename__ = 'conferences'

    conference_id = Column(Integer, primary_key=True)
    name = Column(String)
    league_id = Column(Integer, ForeignKey('leagues.league_id'))


class Divisions(Base):
    __tablename__ = 'divisions'

    division_id = Column(Integer, primary_key=True)
    name = Column(String)
    conference_id = Column(Integer, ForeignKey('conferences.conference_id'))


class Teams(Base):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True)
    name = Column(String)
    season_id = Column(Integer, ForeignKey('seasions.season_id'))
    division_id = Column(Integer, ForeignKey('divisions.division_id'))
    url = Column(String)


class Games(Base):
    __tablename__ = 'games'

    game_id = Column(Integer, primary_key=True)

    start_date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    season_id = Column(Integer, ForeignKey('seasons.season_id'))
    arena_id = Column(Integer, ForeignKey('arenas.arena_id'))
    attendence = Column(Integer)
    home_team_id = Column(Integer, ForeignKey('teams.team_id'))
    away_team_id = Column(Integer, ForeignKey('teams.team_id'))
    reportid = Column(String)
    game_type = Column(Enum('PRE', 'REG', 'POST'))


class Seasons(Base):
    __tablename__ = 'seasons'

    season_id = Column(Integer, primary_key=True)
    name = Column(String)  # Ex. 20142015


class Events(Base):
    __tablename__ = 'events'
    __tableargs__ = (
        CheckConstraint('0 <= elapsed_time <= 1200', name='elapse_time_constaint')
    )

    event_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.game_id'))
    period = Column(Integer)
    strength = Column(Enum('EV', 'PP', 'SH'))
    elapsed_time = Column(Integer)  # Should be bounded between 0-1200 seconds
    event = Column(Enum('PSTR', 'FAC', 'HIT', 'BLOCK', 'MISS', 'SHOT', 'STOP', 'FAC', 'GOAL', 'GIVE', 'BLOCK', 'TAKE', 'PEND', 'GEND', 'PENL'))
    description = Column(String(length=100, convert_unicode=True), nullable=False)
    home_offensive_line = Column(String)  # This is player ids L-C-R
    home_defensive_line = Column(String)  # This is player ids LD-RD
    home_goalie = Column(Integer, ForeignKey('players.player_id'))  # Could also be an extra skater
    away_offensive_line = Column(String)
    away_defensive_line = Column(String)
    away_goalie = Column(Integer, ForeignKey('players.player_id'))  # Could also be an extra skater


class PlayerEvents(Base):
    __tablename__ = 'player_events'

    player_event_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    event_id = Column(Integer, ForeignKey('events.event_id'))
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    position = Column(Enum('L', 'C', 'R', 'LD', 'RD', 'G', 'E'))
