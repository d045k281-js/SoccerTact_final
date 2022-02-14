#Function to draw the pitch
import matplotlib.pyplot as plt
import numpy as np
import sys
import requests
import json
from pandas import json_normalize
from FCPython import createPitch

#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

m_id = str(sys.argv[1])
to_fetch = m_id+'.json'

e_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/"+to_fetch
e_data = json.loads((requests.get(e_site)).text)

l_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/"+to_fetch
l_data = json.loads((requests.get(l_site)).text)

#getting the name of the teams
df = json_normalize(l_data, sep = "_").assign(match_id = m_id)
events = df.loc[df['match_id'] == m_id]
t1 ='a'
for i,event in events.iterrows():
    if(t1=='a'):
        t1 = event['team_name']
    else:
        t2 = event['team_name']

# get the nested structure into a dataframe 
# store the dataframe in a dictionary with the match id as key (remove '.json' from string)
df = json_normalize(e_data, sep = "_").assign(match_id = m_id)

t1_data =  df.loc[df['team_name'] == t1].set_index('id')
t2_data =  df.loc[df['team_name'] == t2].set_index('id')

t1_shots = t1_data.loc[t1_data['type_name'] == 'Shot']
t2_shots = t2_data.loc[t2_data['type_name'] == 'Shot']

(fig1,ax1) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
for i,shots in t1_shots.iterrows():
    x=shots['location'][0]
    y=shots['location'][1]
    
    circleSize=2
    circleSize=np.sqrt(shots['shot_statsbomb_xg'])*8
    
    if (shots['shot_outcome_name']=='Goal'):
        shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")
    else:
        shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")     
        shotCircle.set_alpha(.3)
    ax1.add_patch(shotCircle)

fig1.set_size_inches(10, 7)
#plt.show()
fig1.savefig('./public/analysis/home.png')

(fig2,ax2) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
for i,shots in t2_shots.iterrows():
    x=shots['location'][0]
    y=shots['location'][1]
    
    circleSize=2
    circleSize=np.sqrt(shots['shot_statsbomb_xg'])*8
    
    if (shots['shot_outcome_name']=='Goal'):
        shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="blue")
    else:
        shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="blue")     
        shotCircle.set_alpha(.3)
    ax2.add_patch(shotCircle)

fig2.set_size_inches(10, 7)
#fig.savefig('Output/passes.pdf', dpi=100)
#plt.show()
fig2.savefig('./public/analysis/away.png')