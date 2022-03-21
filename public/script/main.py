from ShotMap import generate_ShotXg
from pass_map import generate_pass
from pass_map import passing_network 
from Event_HeatMap import generate_HeatMap

import sys
import requests
import json
from pandas import json_normalize

m_id = str(sys.argv[1])
team_name = sys.argv[2]
to_fetch = m_id+'.json'

e_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/"+to_fetch
e_data = json.loads((requests.get(e_site)).text)

l_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/"+to_fetch
l_data = json.loads((requests.get(l_site)).text)

#getting the name of the teams
df = json_normalize(l_data, sep = "_").assign(match_id = m_id)
events = df.loc[df['match_id'] == m_id]
# t1 ='a'
# for i,event in events.iterrows():
#     if(t1=='a'):
#         t1 = event['team_name']
#     else:
#         t2 = event['team_name']

#m_id is the match ID
#t1 is first teams name
#t2 is second teams name
#e_data is the event data for that match ID
#l_data is the lineup data for that match ID
generate_ShotXg(m_id,team_name,e_data,l_data)
generate_pass(m_id,team_name,e_data,l_data)
passing_network(m_id, team_name, e_data, l_data)
generate_HeatMap(m_id, team_name, e_data, l_data, event_type= "Pressure")
generate_HeatMap(m_id, team_name, e_data, l_data, event_type= "Pass")
generate_HeatMap(m_id, team_name, e_data, l_data, event_type= "Duel")
