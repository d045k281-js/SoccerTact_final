#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 21:22:59 2022

@author: atifsiddiqui
"""

import sys
import json
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import numpy as np

match_id = sys.argv[1]
home_team = sys.argv[2]
away_team = sys.argv[3]
event_type = sys.argv[4]
event_team = sys.argv[5]

print(match_id)
print(home_team)
print(away_team)
print(event_type)


# call KPI script and put the visualizations in a folder

file_name=str(match_id)+'.json'


with open('/Users/deepak/Documents/SoccerTact/data/events/'+file_name) as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)
    
#get the nested structure into a dataframe 
#store the dataframe in a dictionary with the match id as key (remove '.json' from string)

df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])

print(event_type)


events = df.loc[df['type_name'] == event_type].set_index('id')

pitchLengthX=120
pitchWidthY=80

from FCPython import createPitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')

for i,event in events.iterrows():
    x=event['location'][0]
    y=event['location'][1]
    
    circleSize=1
    team_name=event['team_name']
    
    if (team_name == event_team and team_name == home_team):
        eventCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="blue")
        ax.add_patch(eventCircle)
        
    elif (team_name == event_team and team_name == away_team): 
        eventCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")
        ax.add_patch(eventCircle)
    fig.set_size_inches(10, 7)
fig.savefig('passes.png')
plt.show()




