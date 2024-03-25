import pandas as pd
import requests, json, pprint

stat_mapping = {
    'gamesPlayed': 'GP',
    'mins': 'MIN',
    'pts': 'PTS',
    'fgm': 'FGM',
    'fga': 'FGA',
    'fgp': 'FG%',
    'tptfgm': '3PM',
    'tptfga': '3PA',
    'tptfgp': '3P%',
    'ftm': 'FTM',
    'fta': 'FTA',
    'ftp': 'FT%',
    'OffReb': 'OREB',
    'DefReb': 'DREB',
    'reb': 'REB',
    'ast': 'AST',
    'stl': 'STL',
    'blk': 'BLK'
}