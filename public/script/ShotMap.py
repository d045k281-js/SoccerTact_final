import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

from mplsoccer import Pitch, VerticalPitch, FontManager
from mplsoccer.statsbomb import read_event, EVENT_SLUG
import sys
import requests
import json
from pandas import json_normalize

rcParams['text.color'] = '#c7d5cc'  # set the default text color
plt.style.use('ggplot')

def generate_ShotXg(m_id,t1,t2,e_data,l_data):
    #Size of the pitch in yards (!!!)
    
    
    pitch = VerticalPitch(half = True, pitch_type='statsbomb',pitch_color='grass', line_color='white', stripe=True)  # showing axis labels is optional
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=False, tight_layout=True) 
    # get the nested structure into a dataframe 
    # store the dataframe in a dictionary with the match id as key (remove '.json' from string)

    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    
    t1_data =  df.loc[df['team_name'] == t1].set_index('id')
    t2_data =  df.loc[df['team_name'] == t2].set_index('id')

    t1_shots = t1_data.loc[t1_data['type_name'] == 'Shot']
    t2_shots = t2_data.loc[t2_data['type_name'] == 'Shot']
    
    for i,shots in t1_shots.iterrows():
        x=shots['location'][0]
        y=shots['location'][1]
        
        circleSize=2
        circleSize=np.sqrt(shots['shot_statsbomb_xg'])*1500
        
        if (shots['shot_outcome_name']=='Goal'):
            shotCircle1= pitch.scatter(x, y, marker='football', s= circleSize, edgecolors='blue', c='yellow', ax=ax)
        else:
           shotCircle2= pitch.scatter(x, y, marker='football', s= circleSize, ax=ax)     
            
    # ax.legend(facecolor='#22312b', edgecolor='None', fontsize=5, loc='upper left', handlelength=4)
    #ax.set_title(f'{t1} Shot Map VS {t2}', fontsize=15, color = "black")
    fig.savefig('./public/analysis/t1_shot.png', bbox_inches = 'tight')

    for i,shots in t2_shots.iterrows():
        x=shots['location'][0]
        y=shots['location'][1]
        
        circleSize=2
        circleSize=np.sqrt(shots['shot_statsbomb_xg'])*1500
        
        if (shots['shot_outcome_name']=='Goal'):
            shotCircle1= pitch.scatter(x, y, marker='football', s= circleSize, edgecolors='blue', c='yellow', ax=ax)
        else:
           shotCircle2= pitch.scatter(x, y, marker='football', s= circleSize, ax=ax)     
            
    # ax.legend(facecolor='#22312b', edgecolor='None', fontsize=5, loc='upper left', handlelength=4)
    #ax.set_title(f'{t2} Shot Map VS {t1}', fontsize=15, color = "black")
    fig.savefig('./public/analysis/t2_shot.png', bbox_inches = 'tight')
