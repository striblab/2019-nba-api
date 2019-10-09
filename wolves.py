import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import franchiseplayers
import json, csv

wolves = teams.find_teams_by_state('minnesota')

print(wolves)

print(wolves[0]['id'])

wolves_franchise = franchiseplayers.FranchisePlayers(team_id=wolves[0]['id'])

print(wolves_franchise)

wolves_franchise.get_json()
