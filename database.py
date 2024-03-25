from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    team_abv = db.Column(db.String(3), nullable=False)
    team_city = db.Column(db.String(100), nullable=False)
    team_schedule = db.Column(db.JSON, nullable=False)
    current_streak = db.Column(db.JSON, nullable=False)
    loss = db.Column(db.String(10), nullable=False)
    ppg = db.Column(db.String(10), nullable=False)
    roster = db.Column(db.JSON, nullable=False)
    team_id = db.Column(db.String(10), nullable=False)
    division = db.Column(db.String(100), nullable=False)
    conference_abv = db.Column(db.String(5), nullable=False)
    nba_com_logo2 = db.Column(db.String(200), nullable=False)
    nba_com_logo1 = db.Column(db.String(200), nullable=False)
    espn_logo1 = db.Column(db.String(200), nullable=False)
    oppg = db.Column(db.String(10), nullable=False)
    wins = db.Column(db.String(10), nullable=False)
    conference = db.Column(db.String(100), nullable=False)
    top_performers = db.Column(db.JSON, nullable=False)
    defensive_stats = db.Column(db.JSON, nullable=False)
    offensive_stats = db.Column(db.JSON, nullable=False)


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(100), nullable=False)
    team_code = db.Column(db.String(5))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    player_name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.String(10), db.ForeignKey('teams.team_id'))
    picture = db.Column(db.String(500))
    team = db.relationship('Team', backref='players')

class gamesPerTeam(db.Model):
    __tablename__ = 'gamesPerTeam'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String(10))
    team_code = db.Column(db.String(5))
    games = db.Column(db.JSON, nullable=False)