import requests, os, json
from dotenv import load_dotenv
from database import db, Player, Team, gamesPerTeam
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify

load_dotenv()


def getPlayersInfo():

    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAPlayerList"

    headers = {
        "X-RapidAPI-Key": os.environ.get("API_KEY"),
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)

        players_data = response.json()


    except requests.RequestException as e:
        print("Request failed:", e)
        return []
    
    player_list = []

    for player in players_data['body']:
        first_name, last_name = player['longName'].split(' ', 1)
        player_dict = {
            'playerID': player['playerID'],
            'team_code':player["team"],
            'first_name': first_name.lower(),
            'last_name': last_name.lower(),
            'longName':player["longName"].lower(),
            'teamID': player["teamID"],
            'picture': ''
        }

        player_list.append(player_dict)

    roster_entries = Team.query.with_entities(Team.roster).all()

    teams = [entry[0] for entry in roster_entries]
    

    for player in player_list:
        player_id = player.get('playerID')

        for team_roster in teams:
            for roster_player_id, roster_player_info in team_roster.items():
                    if player['picture'] == '':
                        player['picture'] = roster_player_info.get('nbaComHeadshot')
                        break
    
    
    for player_info in player_list:


        
        if player_info['team_code'] == "":
            player_info['team_code'] = None


        elif player_info['teamID'] == "":
            player_info['teamID'] = None
        

        else:
            player = Player(
                player_id=player_info['playerID'],
                team_code=player_info['team_code'],
                first_name=player_info['first_name'],
                last_name=player_info['last_name'],
                player_name=player_info['longName'],
                team_id=player_info['teamID'],
                picture=player_info['picture']
            )
            db.session.add(player)

    
    db.session.commit()
    
    return player_list



def get_team_info():

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
    

    team_list = []

    for team in teams_data['body']:
        team_dict = {
        'teamAbv': team.get('teamAbv', ''),
        'teamCity': team.get('teamCity', ''),
        'teamSchedule': team.get('teamSchedule', {}),
        'currentStreak': team.get('currentStreak', {}),
        'loss': team.get('loss', ''),
        'ppg': team.get('ppg', ''),
        'teamName': team.get('teamName', ''),
        'Roster': team.get('Roster', {}),
        'teamID': team.get('teamID', ''),
        'division': team.get('division', ''),
        'conferenceAbv': team.get('conferenceAbv', ''),
        'nbaComLogo2': team.get('nbaComLogo2', ''),
        'nbaComLogo1': team.get('nbaComLogo1', ''),
        'espnLogo1': team.get('espnLogo1', ''),
        'oppg': team.get('oppg', ''),
        'wins': team.get('wins', ''),
        'conference': team.get('conference', ''),
        'topPerformers': team.get('topPerformers', {}),
        'defensiveStats': team.get('defensiveStats', {}),
        'offensiveStats': team.get('offensiveStats', {})
    }
        print(team_dict)
        team_list.append(team_dict)

    for team_data in team_list:
        team = Team(
            team_name=team_data.get('teamName', ''),
            team_abv=team_data.get('teamAbv', ''),
            team_city=team_data.get('teamCity', ''),
            team_schedule=team_data.get('teamSchedule', {}),
            current_streak=team_data.get('currentStreak', {}),
            loss=team_data.get('loss', ''),
            ppg=team_data.get('ppg', ''),
            roster=team_data.get('Roster', {}),
            team_id=team_data.get('teamID', ''),
            division=team_data.get('division', ''),
            conference_abv=team_data.get('conferenceAbv', ''),
            nba_com_logo2=team_data.get('nbaComLogo2', ''),
            nba_com_logo1=team_data.get('nbaComLogo1', ''),
            espn_logo1=team_data.get('espnLogo1', ''),
            oppg=team_data.get('oppg', ''),
            wins=team_data.get('wins', ''),
            conference=team_data.get('conference', ''),
            top_performers=team_data.get('topPerformers', {}),
            defensive_stats=team_data.get('defensiveStats', {}),
            offensive_stats=team_data.get('offensiveStats', {})
        )
        db.session.add(team)

    db.session.commit()

    return team_list



def get_all_games():
    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBATeamSchedule"

    teams_list = list(range(1, 31))


    for team in teams_list:
        querystring = {"teamID": team, "season":"2024"}

        headers = {
            "X-RapidAPI-Key": "df1f3de633msh886a64f1e3aac1ap1f1d70jsna2d045d33a90",
            "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)

            games_per_team_data = response.json()
            

        except requests.RequestException as e:
            print("Request failed:", e)
            return []

        all_games_list = []
        team_code = games_per_team_data['body']['team']
        team_id = games_per_team_data['body']['teamID']

        for game in games_per_team_data['body']['schedule']:

            

            game_dict = {

                'gameID': game.get('gameID'),
                'seasonType': game.get('seasonType'),
                'home': game.get('home'),
                'teamIDHome': game.get('teamIDHome'),
                'homePts': game.get('homePts', None),
                'homeResult': game.get('homeResult', None),
                'gameDate': game.get('gameDate'),
                'gameStatus': game.get('gameStatus'),
                'isTournamentGame': game.get('isTournamentGame'),
                'gameTime': game.get('gameTime'),
                'gameTime_epoch': game.get('gameTime_epoch'),
                'neutralSite': game.get('neutralSite'),
                'away': game.get('away'),
                'teamIDAway': game.get('teamIDAway'),
                'awayPts': game.get('awayPts', None),
                'awayResult': game.get('awayResult', None)

            }
            
            game_dict = {a: b for a, b in game_dict.items() if b is not None}
            all_games_list.append(game_dict)

        team_schedule = {
            'schedule': all_games_list
        }

        team_schedule_object = gamesPerTeam(team_id=team_id, team_code=team_code, games=team_schedule)
        
        try:
            with db.session.begin():
                db.session.add(team_schedule_object)
        
        except SQLAlchemyError as e:
                print("An error occurred:", e)
                db.session.rollback()  
        else:
                
                db.session.commit()
                print(f"{team_code} games added!")

    
    return "Success"




