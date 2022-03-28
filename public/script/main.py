from ShotMap import generate_ShotXg
from pass_map import generate_pass
from pass_map import passing_network 
from Event_HeatMap import generate_HeatMap
from timeline import generate_timeline
from team_KPI import getMatchKPI

import sys
import requests
import json
from pandas import json_normalize

m_id = str(sys.argv[1])
#team_name = sys.argv[2]
to_fetch = m_id+'.json'

e_site = "/Users/deepak/Documents/SoccerTact_final/public/data/data/events"+to_fetch
e_data = json.loads(e_site.text)

l_site = "/Users/deepak/Documents/SoccerTact_final/public/data/data/lineups"+to_fetch
l_data = json.loads(l_site.text)

#getting the name of the teams
df = json_normalize(l_data, sep = "_").assign(match_id = m_id)
events = df.loc[df['match_id'] == m_id]
t1 ='a'
for i,event in events.iterrows():
     if(t1=='a'):
         t1 = event['team_name']
     else:
         t2 = event['team_name']

#m_id is the match ID
#t1 is first teams name
#t2 is second teams name
#e_data is the event data for that match ID
#l_data is the lineup data for that match ID

generate_ShotXg(m_id,t1,t2,e_data,l_data)
generate_pass(m_id,t1,t2,e_data,l_data)
passing_network(m_id, t1,t2, e_data, l_data)
generate_HeatMap(m_id, t1,t2, e_data, l_data, event_type= "Pressure")
generate_HeatMap(m_id, t1,t2, e_data, l_data, event_type= "Pass")
generate_HeatMap(m_id, t1,t2, e_data, l_data, event_type= "Duel")
generate_timeline(m_id, t1, e_data, l_data, 't1')
generate_timeline(m_id, t2, e_data, l_data, 't2')
getMatchKPI(m_id, t1, t2, e_data, l_data)

