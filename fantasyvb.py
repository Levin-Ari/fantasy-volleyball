import pandas as pd
import json
import requests

# Import teams from Google Forms
teams = pd.read_csv("teams.csv")

# Import BoostSport API of Big Ten Volleyball Stats
params = {
    'split': 'conf',
    'level': 'season',
    'teams': 'all',
    'category': 'player',
    'section': 'all',
    'conference': 'Big Ten',
    'seasons': '2025',
    'view': 'table',
    'type': 'player',
    'limit': '1000',
    'orderBy': 'default_rank',
    'order': 'asc',
}

response = requests.get('https://engage-api.boostsport.ai/api/sport/wvb/stats/table', params=params)
data = response.json()

# Create DataFrame of players from API
players = []

for player in data['data']:
    row = {}
    row['name'] = player['full_name']
    row['team'] = player['team_market']
    stats = player['data']
    row['sets'] = next((item['periods'] for item in stats if 'periods' in item), None)
    row['assists'] = next((item['assists'] for item in stats if 'assists' in item), None)
    row['kills'] = next((item['kills'] for item in stats if 'kills' in item), None)
    row['digs'] = next((item['digs'] for item in stats if 'digs' in item), None)
    row['blocks'] = next((item['blocks_pts'] for item in stats if 'blocks_pts' in item), None)
    row['aces'] = next((item['aces'] for item in stats if 'aces' in item), None)
    players.append(row)

# Organize and clean the DataFrame
players_df = pd.DataFrame(players)
players_df = players_df.drop_duplicates().reset_index()
players_df = players_df.drop(columns='index', axis=1)

# Clean the data types for the players stats
players_df['sets'] = players_df['sets'].astype(int)
players_df['assists'] = players_df['assists'].astype(int)
players_df['kills'] = players_df['kills'].astype(int)
players_df['digs'] = players_df['digs'].astype(int)
players_df['blocks'] = players_df['blocks'].astype(float)
players_df['aces'] = players_df['aces'].astype(int)

# Calculate fantasy points per player
players_df['points'] = players_df['assists'] + 2*players_df['kills'] + 3*players_df['blocks'] + 3*players_df['digs'] + 10*players_df['aces']
players_df['points per set'] = round(players_df['points'] / players_df['sets'], 1)

# Sort by highest points
players_df = players_df.sort_values(by='points', ascending=False).reset_index()
players_df = players_df.drop(columns='index', axis=1)

# Get the points for each player on fantasy teams
def getpoints(player):
    row = players_df[players_df['name'] == player]
    try:
        points = row['points'].values[0]
        return points
    except:
        return 0

teams['s1_points'] = teams.apply(lambda row: getpoints(row['s1']), axis=1)
teams['h1_points'] = teams.apply(lambda row: getpoints(row['h1']), axis=1)
teams['m1_points'] = teams.apply(lambda row: getpoints(row['m1']), axis=1)
teams['l1_points'] = teams.apply(lambda row: getpoints(row['l1']), axis=1)
teams['s2_points'] = teams.apply(lambda row: getpoints(row['s2']), axis=1)
teams['h2_points'] = teams.apply(lambda row: getpoints(row['h2']), axis=1)
teams['m2_points'] = teams.apply(lambda row: getpoints(row['m2']), axis=1)
teams['w1_points'] = teams.apply(lambda row: getpoints(row['w1']), axis=1)

teams['total points'] = teams.sum(axis=1, numeric_only=True)
teams = teams.sort_values(by='total points', ascending = False).reset_index()
teams = teams.drop(columns='index', axis=1)

# Export to JSON for use in JavaScript
players_df.to_json("players_output.json", orient='records')
teams.to_json("teams_output.json", orient='records')
