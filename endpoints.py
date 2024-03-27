import requests, json
import os
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import time
from database import Player


load_dotenv()


us_eastern = pytz.timezone('US/Eastern')


current_datetime_usa = datetime.now(us_eastern)


current_date = current_datetime_usa.strftime('%Y%m%d')


# ------ Get Live Scores Endpoint -------- #


def get_cached_data(cache_file, expiration):
    """Retrieve cached data if it's not expired."""
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            cached_data = json.load(file)
        if time.time() - cached_data['timestamp'] < expiration:
            return cached_data['data']
    return None


def update_cache(cache_file, data):
    """Update the cache file with new data."""
    timestamp = time.time()
    cached_data = {'timestamp': timestamp, 'data': data}
    with open(cache_file, 'w') as file:
        json.dump(cached_data, file)


def get_live_scores(date):
    """Retrieve live scores data."""
    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAScoresOnly"
    querystring = {"gameDate": date}
    headers = {
        "X-RapidAPI-Key": os.environ.get("API_KEY"),
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        livegamedata = response.json()['body']
        live_games_list = []
        for game_id, game_info in livegamedata.items():
            game_dict = {
                "gameID": game_id,
                "away": game_info["away"],
                "home": game_info["home"],
                "teamIDAway": game_info["teamIDAway"],
                "teamIDHome": game_info["teamIDHome"],
                "awayPts": game_info["awayPts"],
                "homePts": game_info["homePts"],
                "gameClock": game_info["gameClock"],
                "gameStatus": game_info["gameStatus"],
                "gameTime": game_info["gameTime"],
                "gameTime_epoch": game_info["gameTime_epoch"]
            }
            live_games_list.append(game_dict)
        return live_games_list
    except requests.RequestException as e:
        print("Request failed:", e)
        return []


def get_live_games_data():
    """Retrieve live games data."""
    LIVE_GAMES_CACHE_FILE = 'live_games_cache.json'
    LIVE_GAMES_CACHE_EXPIRATION = 43200  # 12 hours
    current_date = datetime.now().strftime('%Y%m%d')
    live_games_cached_data = get_cached_data(LIVE_GAMES_CACHE_FILE, LIVE_GAMES_CACHE_EXPIRATION)
    if live_games_cached_data:
        return live_games_cached_data
    else:
        new_livescores_data = get_live_scores(current_date)
        update_cache(LIVE_GAMES_CACHE_FILE, new_livescores_data)
        return new_livescores_data


# ------ Get Daily Schedule Endpoint -------- #
    

def daily_schedule_api_call(date):


    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAGamesForDate"

    querystring = {"gameDate":date}

    headers = {
        "X-RapidAPI-Key": os.environ.get("API_KEY"),
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        daily_schedule_data = response.json()
        
    except requests.RequestException as e:
        print("Request failed:", e)
        return []
    
    daily_games_list = []

    for game in daily_schedule_data['body']:
        game_dict = {
            'game_id': game['gameID'],
            'teamIDAway': game['teamIDAway'],
            'away': game['away'],
            'teamIDHome': game['teamIDHome'],
            'gameDate': game['gameDate'],
            'home': game['home']
        }

        daily_games_list.append(game_dict)


    return daily_games_list
    

def get_daily_schedule_data():

    """Retrieve daily schedule data for the given US date."""

    DAILY_GAMES_CACHE_FILE = 'daily_schedule_cache.json'

    DAILY_GAMES_CACHE_EXPIRATION = 43200  # 12 hours

    daily_games_cached_data = get_cached_data(DAILY_GAMES_CACHE_FILE, DAILY_GAMES_CACHE_EXPIRATION)

    if daily_games_cached_data:
        return daily_games_cached_data
    
    else:
        new_daily_games_data = daily_schedule_api_call(current_date)
        update_cache(DAILY_GAMES_CACHE_FILE, new_daily_games_data)
        return new_daily_games_data



# -------- Top Performers API Call --------- #

def top_performers_api_call():

    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBATeams"

    querystring = {"schedules":"true","rosters":"true","topPerformers":"true","teamStats":"true","statsToGet":"averages"}

    headers = {
        "X-RapidAPI-Key": os.environ.get("API_KEY"),
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }


    try:
        response = requests.get(url, headers=headers, params=querystring)

        teams_data = response.json()

    except requests.RequestException as e:
        print("Request failed:", e)
        return []
    

    players_and_averages = []

    for team in teams_data['body']:
       
        roster = team['Roster']

        
        for player_id, player_info in roster.items():
            
            player_name = player_info['longName']

            if 'stats' in player_info:
                
                player_stats = player_info['stats']
            elif 'player' in player_info and 'stats' in player_info['player']:
                player_stats = player_info['player']['stats']
            else:
                
                print(f"No 'stats' key found for player: {player_info}")
                player_stats = None  

            
            player_data = {
                'team': team['teamName'],
                'teamID': player_info['teamID'],
                'college': player_info['college'],
                'birthday': player_info['bDay'],
                'picture': player_info['espnHeadshot'],
                'position': player_info['pos'],
                'weight': player_info['weight'],
                'height': player_info['height'],
                'player_id': player_id,
                'player_name': player_name,
                'stats': player_stats
            }

            
            players_and_averages.append(player_data)

    
    return players_and_averages


def get_player_stats_averages():

    """Retrieve NBA players stats and averages"""

    PLAYER_STATS_AVERAGES_CACHE_FILE = 'player_stats_averages.json'

    PLAYER_STATS_AVERAGES_CACHE_EXPIRATION = 43200  

    PLAYERS_STATS_AVERAGES_DATA = get_cached_data(PLAYER_STATS_AVERAGES_CACHE_FILE, PLAYER_STATS_AVERAGES_CACHE_EXPIRATION)

    if PLAYERS_STATS_AVERAGES_DATA:
        return PLAYERS_STATS_AVERAGES_DATA
    
    else:
        NEW_PLAYER_STATS_AVERAGES_DATA = top_performers_api_call()
        update_cache(PLAYER_STATS_AVERAGES_CACHE_FILE, NEW_PLAYER_STATS_AVERAGES_DATA)
        return NEW_PLAYER_STATS_AVERAGES_DATA


test_players_avgs = get_player_stats_averages()


def find_top_performers(player_stats_list, stats_to_include, min_games=50, num_players=5):
    """
    Find the top performers based on a given statistic.
    
    Args:
    - player_stats_list: List of dictionaries containing player information and statistics.
    - stat: The statistic based on which to find the top performers.
    - num_players: Number of top performers to return (default is 5).
    
    Returns:
    - List of top performers sorted based on the specified statistic.
    """
    
    filtered_players = [player for player in player_stats_list if player is not None and player.get('stats') is not None 
                        and 
                        int(player['stats'].get('gamesPlayed', 0)) >= min_games]
    

    if not filtered_players:
        return []
    

    sorted_players = sorted(
        filtered_players,
        key=lambda x: 
        tuple(float(x.get('stats', {}).get(stat, 0)) 
        for stat in stats_to_include),
        reverse=True
    ) 


    return sorted_players[:num_players]


# -------- Injury Report API Call --------- #


def get_injury_report_api_call():
    """Retrieve injury report data."""
    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAInjuryList"

    headers = {
        "X-RapidAPI-Key": os.environ.get("API_KEY"),
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }

    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        injury_report_data = response.json()['body']
        injury_report_list = []
        


    except requests.RequestException as e:
        print("Request failed:", e)
        return []
    

    for report in injury_report_data:
        player_id = report['playerID']
        player = Player.query.filter_by(player_id=player_id).first()

        if player:
            report_dict = {
                'designation': report['designation'],
                'injDate': report['injDate'],
                'playerID':player_id,
                'description':report['description'],
                'player_name': player.player_name,
                'team_id': player.team_id,
                'team_code':player.team_code}
                

            injury_report_list.append(report_dict)

    
    return injury_report_list
    


def get_injury_list_data():

    """Retrieve NBA players injury reports"""

    PLAYER_INJURY_REPORTS_CACHE_FILE = 'injury_report_cache.json'

    PLAYER_INJURY_REPORTS_CACHE_EXPIRATION = 43200  

    PLAYER_INJURY_REPORT_DATA = get_cached_data(PLAYER_INJURY_REPORTS_CACHE_FILE, PLAYER_INJURY_REPORTS_CACHE_EXPIRATION)

    if PLAYER_INJURY_REPORT_DATA:
        
        return PLAYER_INJURY_REPORT_DATA
    
    else:
        NEW_PLAYER_INJURY_REPORTS_DATA = get_injury_report_api_call()
        update_cache(PLAYER_INJURY_REPORTS_CACHE_FILE, NEW_PLAYER_INJURY_REPORTS_DATA)
        return NEW_PLAYER_INJURY_REPORTS_DATA
