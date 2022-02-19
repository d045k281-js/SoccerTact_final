#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:19:23 2022

@author: atifsiddiqui
"""

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
from urllib.request import urlopen

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from PIL import Image




def generate_passMap(m_id,t1,t2,e_data,l_data, name):
    #Size of the pitch in yards (!!!)
    
    
    pitch = Pitch(pitch_type='statsbomb',axis=True, label=True,pitch_color='grass', line_color='white', stripe=True)  # showing axis labels is optional
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=False, tight_layout=True) 
    # get the nested structure into a dataframe 
    # store the dataframe in a dictionary with the match id as key (remove '.json' from string)

    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    
    df_new = df.loc[df['type_name'] == 'Pass'].set_index('id')

        
    passes = []
    name_req = str(name)
    
    for i, event in df_new.iterrows():
        if (event['player_name'] == name_req):
            timestamp = event['timestamp']
            period = event['period']
            x=event['location'][0]
            y=event['location'][1]
            dx=event['pass_end_location'][0]
            dy=event['pass_end_location'][1]
            outcome_name = event['pass_outcome_name']
            passes.append([period,timestamp,x,y,dx,dy,outcome_name])
    df_pass = pd.DataFrame(passes, columns=['period', 'time','x', 'y', 'end_x', 'end_y', 'outcome_name'])
    
    
    for i, event in df_pass.iterrows():
        x=event['x']
        y=event['y']
        dx=event['end_x']
        dy=event['end_y']
        outcome_name = event['outcome_name']
        
        if(outcome_name == "Incomplete" or outcome_name == "Out" or outcome_name =="Pass Offside" or outcome_name == "Unknown"):
            lc1 = pitch.arrows(x, y, dx, dy ,width=5,
             headwidth=10, headlength=10, color='#ba4f45', ax=ax)
        else: 
            lc2 = pitch.arrows(x, y, dx, dy ,lw=5,width=5,
             headwidth=10, headlength=10, color='#ad993c', ax=ax)
        
    ax.legend(facecolor='#22312b', edgecolor='None', fontsize=5, loc='upper left', handlelength=4)

# Set the title
    ax.set_title(f'{name_req} passes vs {t2}', fontsize=10)
    plt.show()

def generate_possesion(m_id,t1,t2,e_data,l_data, name):
    flamingo_cmap = LinearSegmentedColormap.from_list("Flamingo - 10 colors",
                                                  ['#e3aca7', '#c03a1d'], N=10)
    pitch = VerticalPitch(line_color='#000009', line_zorder=2, pitch_color='white')
    fig, ax = pitch.draw(figsize=(4.4, 6.4))
   
    
    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    df = df[df['location'].notna()]

    name_req = str(name) 
    
    hex = []
   
    for i, event in df.iterrows():
        if (event['player_name'] == name_req):
            x=event['location'][0]
            y=event['location'][1]
            hex.append([x,y])
    df = pd.DataFrame(hex, columns = ['x', 'y'])
    
    hexmap = pitch.hexbin(df.x, df.y, ax=ax, edgecolors='#f4f4f4',
                      gridsize=(8, 8), cmap=flamingo_cmap)
    plt.show()
    
def generate_Shots(m_id,t1,t2,e_data,l_data, name):
    pitch = VerticalPitch(half = True, pitch_type='statsbomb',axis=True, label=True,pitch_color='grass', line_color='white', stripe=True)  # showing axis labels is optional
    fig, ax = pitch.draw(figsize=(8, 6), constrained_layout=False, tight_layout=True) 
    
    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    df_new = df.loc[df['type_name'] == 'Shot'].set_index('id')
    
    name_req = str(name) 
    
    shots = []
    
    for i, event in df_new.iterrows():
        if (event['player_name'] == name_req):
            timestamp = event['timestamp']
            period = event['period']
            x=event['location'][0]
            y=event['location'][1]
            dx=event['shot_end_location'][0]
            dy=event['shot_end_location'][1]
            outcome_name = event['shot_outcome_name']
            shotXG = event['shot_statsbomb_xg'] 
            shots.append([x,y,outcome_name, shotXG])
    df = pd.DataFrame(shots,columns = ['x', 'y', 'outcome', 'shotXG'])
             
    for i, event in df.iterrows():
        circleSize=2
        circleSize=np.sqrt(event['shotXG'])*1500
        if (event['outcome'] =='Goal'):
            shotCircle1= pitch.scatter(event['x'], event['y'], marker='football', s= circleSize, edgecolors='blue', c='yellow', ax=ax)
        else:
            shotCircle2= pitch.scatter(event['x'], event['y'], marker='football', s= circleSize, ax=ax)     
            
    ax.legend(facecolor='#22312b', edgecolor='None', fontsize=5, loc='upper left', handlelength=4)
    plt.show()

