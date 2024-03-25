from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os, requests
from database import db, Player, Team, gamesPerTeam
from database_api_endpoints import getPlayersInfo, get_team_info, get_all_games
from endpoints import get_live_games_data, get_daily_schedule_data, get_player_stats_averages, find_top_performers, get_injury_list_data, get_injury_report_api_call
from main import stat_mapping
import mysql.connector
from sqlalchemy import text
from datetime import datetime
from flask_caching import Cache
from datetime import timedelta


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.environ.get('user')}:{os.environ.get('password')}@{os.environ.get('host')}/{os.environ.get('database')}"
db.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        search_query = request.form.get('search_query')
        matching_players = Player.query.filter(Player.player_name.ilike(f'%{search_query}%')).all()
        
        return redirect(url_for('search_results', query=search_query))



    live_games = get_live_games_data()
    test_players_avgs = get_player_stats_averages()
    top_players = find_top_performers(test_players_avgs, ['pts', 'reb', 'ast', 'stl', 'OffReb', 'DefReb', 'blk', 'fgp', 'trueShootingPercentage', 
                                                      'fgm', 'ftp', 'fta', 'ftm', 'tptfga', 'tptfgp', 'tptfgm', 'mins', 'gamesPlayed'])
    
    new_sm = stat_mapping
    injury_report_list = get_injury_list_data()
    for report in injury_report_list:
        report['injDate'] = datetime.strptime(report['injDate'], '%Y%m%d').strftime('%B %d, %Y')

    return render_template("index.html", live_games=live_games, top_players=top_players, new_sm=new_sm, injury_report_list=injury_report_list)


@app.route('/search_results/<query>')
def search_results(query):
    
    
    all_teams_and_games = gamesPerTeam.query.all()
    all_teams_data = Team.query.all()
    matching_players = Player.query.filter(Player.player_name.ilike(f'%{query}%')).all()
    playerInfo = get_player_stats_averages()
    
    active_player_ids = [player['player_id'] for player in playerInfo]

    filtered_players = [player for player in matching_players if player.player_id in active_player_ids]

    return render_template('search_results.html', query=query, players=filtered_players)



@app.route('/player/<string:player_id>')
@cache.cached(timeout=86400)
def player_profile(player_id):
    playerID = Player.query.filter_by(player_id=player_id).first()
    
    player_data = cache.get(player_id)
    all_player_games = []
    if player_data is None:
        

        url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAGamesForPlayer"
        querystring = {"playerID": player_id, "season": "2024"}
        headers = {
            "X-RapidAPI-Key": os.environ.get("API_KEY"),
            "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        player_data = response.json()['body']
        
        
        for game_id, game_info in player_data.items():
                game_date_str = game_id.split('_')[0]
                formatted_game_date = f"{game_date_str[:4]}/{game_date_str[4:6]}/{game_date_str[6:]}"
                one_game = {
            'blk': game_info.get('blk'),
            'OffReb': game_info.get('OffReb'),
            'ftp': game_info.get('ftp'),
            'DefReb': game_info.get('DefReb'),
            'plusMinus': game_info.get('plusMinus'),
            'stl': game_info.get('stl'),
            'pts': game_info.get('pts'),
            'tech': game_info.get('tech'),
            'team': game_info.get('team'),
            'TOV': game_info.get('TOV'),
            'fga': game_info.get('fga'),
            'ast': game_info.get('ast'),
            'tptfgp': game_info.get('tptfgp'),
            'teamAbv': game_info.get('teamAbv'),
            'mins': game_info.get('mins'),
            'fgm': game_info.get('fgm'),
            'fgp': game_info.get('fgp'),
            'reb': game_info.get('reb'),
            'teamID': game_info.get('teamID'),
            'tptfgm': game_info.get('tptfgm'),
            'fta': game_info.get('fta'),
            'tptfga': game_info.get('tptfga'),
            'longName': game_info.get('longName'),
            'PF': game_info.get('PF'),
            'player_id': game_info.get('playerID'),
            'ftm': game_info.get('ftm'),
            'game_id': game_info.get('game_infoID'),
            'fantasyPoints': game_info.get('fantasyPoints'),
            'gameDate': formatted_game_date
    }       
                all_player_games.append(one_game)


    
    timeout_seconds = timedelta(hours=24).total_seconds()
    cache.set(player_id, player_data, timeout=timeout_seconds)


    if playerID:

        individual_player = []
        test_players_avgs = get_player_stats_averages()
        

        for player in test_players_avgs:
            
            if player['player_id'] == player_id:
                individual_player.append(player)
        

        team_data = Team.query.filter_by(team_name=individual_player[0]['team']).first()
        birthday_date = datetime.strptime(individual_player[0]['birthday'], '%m/%d/%Y')
        current_date = datetime.now()
        age = current_date.year - birthday_date.year - ((current_date.month, current_date.day) < (birthday_date.month, birthday_date.day))
        return render_template("player_profile.html", player=individual_player[0], team=team_data, age=age, players_games=all_player_games)
    else:
        
        return render_template("player_not_found.html")







"""API for database/frontend calls"""

@app.route("/api/add_players")
def add_players():
    getPlayersInfo()

    return jsonify("Success")



@app.route("/api/daily-games")
def get_daily_games():
    live_games = get_live_games_data()
    sorted_games = sorted(live_games, key=lambda x: x['gameTime_epoch'])

    return jsonify(sorted_games)




@app.route("/api/get_all_games")
def get_all_games_for_each_team():

    get_all_games()

    return jsonify("Success")


@app.route("/api/top-performers")
def get_top_performers():

    test_players_avgs = get_player_stats_averages()
    top_players = find_top_performers(test_players_avgs, ['pts', 'reb', 'ast', 'stl', 'OffReb', 'DefReb', 'blk', 'fgp', 'trueShootingPercentage', 
                                                      'fgm', 'ftp', 'fta', 'ftm', 'tptfga', 'tptfgp', 'tptfgm', 'mins', 'gamesPlayed'])
    
    roster_entries = Team.query.with_entities(Team.roster).all()

    teams = [entry[0] for entry in roster_entries]
    

    for player in top_players:
        player_id = player.get('player_id')

        for team_roster in teams:
            for roster_player_id, roster_player_info in team_roster.items():
                if roster_player_id == player_id:
                    player['nbaComHeadshot'] = roster_player_info.get('nbaComHeadshot')
                    break
    
    return jsonify(top_players)
    


@app.route("/api/injury-report")
def get_injury_report():
    injury_report_list = get_injury_list_data()
    

    roster_entries = Team.query.with_entities(Team.roster).all()

    teams = [entry[0] for entry in roster_entries]
    

    for player in injury_report_list:
        player_id = player.get('playerID')

        for team_roster in teams:
            for roster_player_id, roster_player_info in team_roster.items():
                if roster_player_id == player_id:
                    player['nbaComHeadshot'] = roster_player_info.get('nbaComHeadshot')
                    break
    return jsonify(injury_report_list)



@app.route("/api/adding_pictures")
def add_pictures():
    players_without_picture = Player.query.filter(Player.picture == '').all()
    empty_players_list = []
    for player in players_without_picture:
        empty_player = {
            'player_id': player.player_id,
            'player_name': player.player_name,
            'picture': player.picture
        }
        empty_players_list.append(empty_player)
    
    

    API_URL = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAPlayerInfo"
    HEADERS = {
        "X-RapidAPI-Key": os.environ.get("API_KEY"),
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }

    
    for empty_player in empty_players_list:
        player_name = empty_player['player_name']

       
        response = requests.get(API_URL, headers=HEADERS, params={"playerName": player_name})
        if response.status_code == 200:
            
            player_info_list =  player_info_list = response.json().get('body', [])
            player_info = player_info_list[0]

            
            picture_link = player_info.get('nbaComHeadshot')
            if picture_link:
                
                empty_player['picture'] = picture_link

                
                player = Player.query.filter_by(player_name=player_name).first()
                if player:
                    player.picture = picture_link
                    
                    db.session.commit()
                else:
                    print(f"Player with name '{player_name}' not found in the database")
            else:
                print(f"No picture link found for player with name '{player_name}'")
        else:
            print(f"Failed to retrieve player information for player with name '{player_name}'")

    return jsonify(f"{len(empty_players_list)}")


