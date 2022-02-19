#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 00:48:06 2022

@author: atifsiddiqui
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from mplsoccer import Pitch, VerticalPitch, FontManager
import json
from pandas import json_normalize
from urllib.request import urlopen

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from PIL import Image

def generate_pass(m_id,t1,t2,e_data,l_data):
    
    pitch = VerticalPitch(pitch_type='statsbomb',axis=True, line_zorder=2, line_color='#c7d5cc', pitch_color='#22312b')  # showing axis labels is optional
    bins = (6, 4)
    fig, ax = pitch.draw(figsize=(8, 6), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312b')
    
    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)  
    t1_data =  df.loc[df['team_name'] == t1].set_index('id')
    t2_data =  df.loc[df['team_name'] == t2].set_index('id')

    t1_pass = t1_data.loc[t1_data['type_name'] == 'Pass']
    t2_pass = t2_data.loc[t2_data['type_name'] == 'Pass']
    
    passes = []
    
    for i, event in t1_pass.iterrows():
        timestamp = event['timestamp']
        period = event['period']
        x=event['location'][0]
        y=event['location'][1]
        dx=event['pass_end_location'][0]
        dy=event['pass_end_location'][1]
        outcome_name = event['pass_outcome_name']
        passes.append([period,timestamp,x,y,dx,dy,outcome_name])
    df_pass = pd.DataFrame(passes, columns=['period', 'time','x', 'y', 'end_x', 'end_y', 'outcome_name'])
    
    
    bs_heatmap = pitch.bin_statistic(df_pass.x, df_pass.y, statistic='count', bins=bins)
    hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='Blues')
# plot the pass flow map with a single color ('black') and length of the arrow (5)
    fm = pitch.flow(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y,
                color='black', arrow_type='same',
                arrow_length=5, bins=bins, ax=ax)
    ax.set_title(f'{t1} pass flow map vs {t2}', fontsize=30, pad=-20)
    plt.show()
    
    passes_2 = []
    
    for i, event in t2_pass.iterrows():
        timestamp = event['timestamp']
        period = event['period']
        x=event['location'][0]
        y=event['location'][1]
        dx=event['pass_end_location'][0]
        dy=event['pass_end_location'][1]
        outcome_name = event['pass_outcome_name']
        passes_2.append([period,timestamp,x,y,dx,dy,outcome_name])
    df_pass = pd.DataFrame(passes_2, columns=['period', 'time','x', 'y', 'end_x', 'end_y', 'outcome_name'])
    
    
    bs_heatmap = pitch.bin_statistic(df_pass.x, df_pass.y, statistic='count', bins=bins)
    hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='Blues')
# plot the pass flow map with a single color ('black') and length of the arrow (5)
    fm = pitch.flow(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y,
                color='black', arrow_type='same',
                arrow_length=5, bins=bins, ax=ax)
    ax.set_title(f'{t2} pass flow map vs {t1}', fontsize=30, pad=-20)
    plt.show()