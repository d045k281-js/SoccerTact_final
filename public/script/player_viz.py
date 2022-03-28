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
from PIL import Image

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
from mplsoccer import PyPizza, add_image, FontManager

font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))


def generate_passMap(m_id,t1,t2,e_data,l_data, name):
    #Size of the pitch in yards (!!!)
    
    
    pitch = Pitch(pitch_type='statsbomb',axis=False, label=False,pitch_color='grass', line_color='white', stripe=True)  # showing axis labels is optional
    fig3, ax = pitch.draw(figsize=(10, 8), constrained_layout=False, tight_layout=True) 
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
    #ax.set_title(f'{name_req} passes vs {t2}', fontsize=15, y = 1.0)
    fig3.text(
        0.07, 0.09, "Complete       Incomplete", size=14,
        fontproperties=font_bold.prop, color="black"
    )
    fig3.patches.extend([
    plt.Rectangle(
        (0.04, 0.09), 0.025, 0.021, fill=True, color="#ad993c",
        transform=fig3.transFigure, figure=fig3
    ),
    plt.Rectangle(
        (0.16, 0.09), 0.025, 0.021, fill=True, color="#ba4f45",
        transform=fig3.transFigure, figure=fig3
    ),
])
    fig3.savefig('./public/ply_analysis/pass.png', bbox_inches = 'tight')
    #fig3.savefig('/Users/atifsiddiqui/Desktop/pass.png')

def generate_possesion(m_id,t1,t2,e_data,l_data, name):
    flamingo_cmap = LinearSegmentedColormap.from_list("Flamingo - 10 colors",
                                                  ['#e3aca7', '#c03a1d'], N=10)
    pitch = Pitch(line_color='#000009', line_zorder=2, pitch_color='white')
    fig, ax = pitch.draw(figsize=(10, 8))
   
    
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
    #ax.set_title(f'{name_req} possesion vs {t2}', fontsize=15, y = 1.0)
    fig.savefig('./public/ply_analysis/poss.png', bbox_inches = 'tight')
    
def generate_Shots(m_id,t1,t2,e_data,l_data, name):
    pitch = Pitch(half = True, pitch_type='statsbomb',axis=False, label=False,pitch_color='grass', line_color='white', stripe=True)  # showing axis labels is optional
    fig2, ax = pitch.draw(figsize=(10, 8), constrained_layout=False, tight_layout=True) 
    
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
    #ax.set_title(f'{name_req} Shots vs {t2}', fontsize=15, y = 1.0)
    fig2.savefig('./public/ply_analysis/shot.png', bbox_inches = 'tight')
  
def generatePlayerKPI(m_id,t1,t2,e_data,l_data, name):
    params = []
    values = []
    df = pd.json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    
    name_req = str(name)
    
    goals = 0 
    shots = 0 
    pass_completed = 0 
    #can extend to include different types of passes 
    pressure = 0
    miscontrol = 0
    foul_won = 0
    foul_committed = 0 
    duel_won = 0
    dribble = 0 
    dispossessed = 0 
    carry = 0
    ball_recovery = 0 
    
    for i, events in df.iterrows():
        if events['player_name']==name_req:
            if events['type_name'] == 'Shot':
                if events['shot_outcome_name'] == 'Goal':
                    goals = goals + 1
                    shots = shots + 1
                else: 
                    shots = shots + 1
            if events['type_name'] == 'Pass':
                if events['pass_outcome_name'] != 'Incomplete':
                    pass_completed = pass_completed + 1
            if events['type_name'] == 'Pressure':
                pressure = pressure + 1
            if events['type_name'] == 'Miscontrol':
                miscontrol = miscontrol + 1
            if events['type_name'] == 'Foul Won':
                foul_won = foul_won + 1
            if events['type_name'] == 'Foul Committed':
                foul_committed = foul_committed + 1
            if events['type_name'] == 'Duel':
                if events['duel_outcome_name'] == 'Won' or events['duel_outcome_name'] =='Success In Play':
                    duel_won = duel_won + 1
            if events['type_name'] == 'Dribble':
                dribble = dribble + 1
            if events['type_name'] == 'Dispossessed':
                dispossessed = dispossessed + 1
            if events['type_name'] == 'Carry':
                carry = carry + 1
            if events['type_name'] == 'Ball Recovery':
                ball_recovery = ball_recovery + 1

                
    values.append([goals,shots,pass_completed,pressure,miscontrol,foul_won,foul_committed,duel_won,dribble,dispossessed,carry,ball_recovery])       
    values= [item for sublist in values for item in sublist]
    
    params = ["Goals","Shots","Pass Completed","Pressure","Miscontrol","Foul Won","Foul Comminted","Duel Won","Dribbles" ,"Dispossessed","Carry","Ball Recovery"]
    
    # color for the slices and text
    slice_colors = ["#1A78CF"] * 4 + ["#FF9300"] * 4 + ["#D70232"] * 4
    text_colors =  ["black"] * 12
    
    baker = PyPizza(
    params=params,                  # list of parameters
    background_color="white",     # background color
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_color="#000000",    # color for last line
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=0,              # linewidth for other circles
    inner_circle_size=30            # size of inner circle
    )
    
    # plot pizza
    fig4, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(8, 8.5),                # adjust the figsize according to your need
        color_blank_space="same",        # use the same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
        edgecolor="#000000", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
    kwargs_params=dict(
        color="black", fontsize=12,
        fontproperties=font_bold.prop, va="center"
        ),                               # values to be used when adding parameter labels
    kwargs_values=dict(
        color="black", fontsize=12,
        fontproperties=font_bold.prop, zorder=3,
        bbox=dict(
            edgecolor="black", facecolor="black",
            boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values labels
    )
    #fig4.text( 0.515, 0.875, "Key Performance Indicators", size=16, ha="center", fontproperties=font_bold.prop, color="#000000")
    #ax.set_title(f'{name} KPI', fontsize=12, color = "black")
    fig4.savefig('./public/ply_analysis/KPI.png', transparent = True, bbox_inches = 'tight')
    #fig4.savefig('/Users/atifsiddiqui/Desktop/pass.png', transparent = True)
