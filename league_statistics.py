import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats
import json, csv

all_teams = teams.get_teams()

team_info = {'data': []}
for team in all_teams:
    new_team = {}
    new_team['id'] = team['id']
    new_team['abbrev'] = team['abbreviation']
    new_team['city'] = team['city']
    team_info['data'].append(new_team)

team_info['data'][0]['id']
len(team_info['data'])

team_resp = {'data': []}
i = 0

for i in range(len(team_info['data'])):
    obj = teamyearbyyearstats.TeamYearByYearStats(team_id=team_info['data'][i]['id'])
    new_resp = obj.get_normalized_dict()
    df = pd.DataFrame.from_dict(new_resp['TeamStats'], orient='columns')
    df_1979 = df['YEAR'] >= "1979-80"
    df = df[df_1979]
    team_resp['data'].append(df)

df1979 = pd.read_csv('./data/season1979.csv')
df1980 = pd.read_csv('./data/season1980.csv')
df1981 = pd.read_csv('./data/season1981.csv')

df1979_fg3 = df1979['3PA'].sum()
df1980_fg3 = df1980['3PA'].sum()
df1981_fg3 = df1981['3PA'].sum()

df1979_fga = df1979['FGA'].sum()
df1980_fga = df1980['FGA'].sum()
df1981_fga = df1981['FGA'].sum()

df1979_3pct = df1979_fg3 / df1979_fga
df1980_3pct = df1980_fg3 / df1980_fga
df1981_3pct = df1981_fg3 / df1981_fga


counter = len(team_resp['data']) - 1
c = 0
for c in range(counter):
    file_name = team_info['data'][c]['abbrev'] + '.csv'
    team_resp['data'][c].to_csv('./data/%s' % file_name)

league_stats = pd.concat(team_resp['data'])
total_3pta = league_stats.groupby('YEAR').FG3A.sum().reset_index()

total_3pta.at[0, 'FG3A'] = df1979_fg3
total_3pta.at[1, 'FG3A'] = df1980_fg3
total_3pta.at[2, 'FG3A'] = df1981_fg3
total_3pta.to_csv('./data/total_3pta.csv')

total_fga = league_stats.groupby('YEAR').FGA.sum().reset_index()
total_fga.at[0, 'FGA'] = df1979_fga
total_fga.at[1, 'FGA'] = df1980_fga
total_fga.at[2, 'FGA'] = df1981_fga
total_fga.to_csv('./data/total_fga.csv')

league_3pct = pd.merge(total_3pta, total_fga, on="YEAR")
league_3pct['pct_of_a'] = league_3pct['FG3A'] / league_3pct['FGA']
league_3pct.to_csv('./data/pct.csv')

three_pt_pct = league_stats.groupby('YEAR').FGA.sum().reset_index()

atlanta = teamyearbyyearstats.TeamYearByYearStats(team_id=team_info['data'][0]['id'])

atlanta_resp = atlanta.get_normalized_dict()

print(atlanta_resp['TeamStats'])

df = pd.DataFrame.from_dict(atlanta_resp['TeamStats'], orient='columns')

df.to_csv('./data/test.csv')

atl_1979 = df['YEAR'] >= "1979-80"
print(atl_1979)
