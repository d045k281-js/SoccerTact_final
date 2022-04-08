
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import dataframe_image as dfi
from pandas import json_normalize
import json
import sys
import requests
m_id = str(sys.argv[1])
#team_name = sys.argv[2]
to_fetch = m_id+'.json'

# e_site = "/Users/deepak/Documents/SoccerTact_final/public/data/data/events/"+to_fetch
# e_data=open('/Users/deepak/Documents/SoccerTact_final/public/data/data/events/'+to_fetch, "r")
with open('./public/data/data/events/'+to_fetch , encoding="utf-8") as e_site:
    e_data = json.load(e_site)

# l_site = "/Users/deepak/Documents/SoccerTact_final/public/data/data/lineups/"+to_fetch
# l_data = json.loads((requests.get(l_site)).text)
# l_data=open('/Users/deepak/Documents/SoccerTact_final/public/data/data/lineups/'+to_fetch, "r")
with open('./public/data/data/lineups/'+to_fetch, encoding="utf-8") as l_site:
    l_data = json.load(l_site)


#getting the name of the teams
df = json_normalize(l_data, sep = "_").assign(match_id = m_id)
events = df.loc[df['match_id'] == m_id]
t1 ='a'
for i,event in events.iterrows():
     if(t1=='a'):
         t1 = event['team_name']
     else:
         t2 = event['team_name']

#Size of the pitch in yards (!!!)
def getMatchKPI(m_id, t1, t2, e_data):
    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    
    t1_data =  df.loc[df['team_name'] == t1].set_index('id')
    t2_data =  df.loc[df['team_name'] == t2].set_index('id')

    possession = []

    gdp_dict = {t1 : [],
                'Match details': ['Goals','total_shots','total_passes','total_corners','total_freekicks','total_offside'],
               t2: []}
    
    total_shots = 0
    total_passes = 0 
    total_corners = 0
    total_freekicks = 0
    duration = 0
    total_offside = 0
    goals = 0 

    for i, events in t1_data.iterrows():
        if (not pd.isna(events['duration'])):
            duration+=events['duration']
            
        if (events['type_name'] == "Shot"):
            total_shots = total_shots + 1
            if(events['shot_outcome_name'] == "Goal"):
                goals+=1
        elif (events['type_name'] == "Pass"):
            total_passes = total_passes + 1
            if (events['pass_type_name'] == "Corner"):
                total_corners = total_corners + 1
            if (events['pass_type_name'] == 'Free Kick'):
                total_freekicks = total_freekicks + 1
            if (events['pass_outcome_name'] == 'Pass Offside'):
                total_offside = total_offside + 1
        if (events['type_name'] == "Offside"):
            total_offside = total_offside + 1
    possession.append(duration)
            
    gdp_dict[t1].extend([goals,int(total_shots),total_passes,total_corners,total_freekicks,total_offside]) 

    total_shots = 0
    total_passes = 0
    total_corners = 0
    total_freekicks = 0
    duration = 0
    total_offside = 0
    goals = 0
    for i, events in t2_data.iterrows():
        if (not pd.isna(events['duration'])):
            duration+=events['duration']
            
        if (events['type_name'] == "Shot"):
            total_shots = total_shots + 1
            if(events['shot_outcome_name'] == "Goal"):
                goals+=1
        elif (events['type_name'] == "Pass"):
            total_passes = total_passes + 1
            if (events['pass_type_name'] == "Corner"):
                total_corners = total_corners + 1
            if (events['pass_type_name'] == 'Free Kick'):
                total_freekicks = total_freekicks + 1
            if (events['pass_outcome_name'] == 'Pass Offside'):
                total_offside = total_offside + 1
        if (events['type_name'] == "Offside"):
            total_offside = total_offside + 1
   
            
    gdp_dict[t2].extend([goals,int(total_shots),total_passes,total_corners,total_freekicks,total_offside]) 
    possession.append(duration)

    totalPossession = sum(possession) 
    homePossession = int((possession[0]/totalPossession)*100)
    awayPossession = 100 - homePossession
    gdp_dict[t2].insert(0,awayPossession)
    gdp_dict[t1].insert(0,homePossession)
    gdp_dict['Match details'].insert(0,"possession")
    data = pd.DataFrame(gdp_dict)
    data = data. set_index([ t1 ,'Match details',t2])
    dfi.export(data, './public/analysis/teamKPI.png')
# import requests
# l_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/18245.json"
# l_data = json.loads((requests.get(l_site)).text)
# getMatchKPI("18245", 'Real Madrid', "Liverpool", l_data)

getMatchKPI(m_id, t1, t2, e_data)