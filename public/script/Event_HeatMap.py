#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 21:22:59 2022

@author: atifsiddiqui
"""

import sys
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
from mplsoccer import Pitch, VerticalPitch, FontManager

import requests
import json
from pandas import json_normalize

path_eff = [path_effects.Stroke(linewidth=1.5, foreground='black'),
            path_effects.Normal()]

def generate_HeatMap(m_id, t1, e_data, l_data, event_type):
    
    pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#f4edf0')
    fig, ax = pitch.draw(figsize=(4.125, 6))
    fig.set_facecolor('#f4edf0')
    
    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    
    t1_data =  df.loc[df['team_name'] == t1].set_index('id')

    t1_event_heat = t1_data.loc[t1_data['type_name'] == event_type]
    
    heat = [] 
    
    for i, event in t1_event_heat.iterrows():
        x=event['location'][0]
        y=event['location'][1]
        heat.append([x,y])
    df = pd.DataFrame(heat, columns = ['X', 'Y'])
    
    bin_x = np.linspace(pitch.dim.left, pitch.dim.right, num=7)
    bin_y = np.sort(np.array([pitch.dim.bottom, pitch.dim.six_yard_bottom,
                          pitch.dim.six_yard_top, pitch.dim.top]))
    
    bin_statistic = pitch.bin_statistic(df.X, df.Y, statistic='count', bins=(bin_x, bin_y), normalize=True )
    
    pitch.heatmap(bin_statistic, ax=ax, cmap='Reds', edgecolor='#f9f9f9')
    labels2 = pitch.label_heatmap(bin_statistic, color='#f4edf0', fontsize=18,
                              ax=ax, ha='center', va='center',
                              str_format='{:.0%}', path_effects=path_eff)
    ax.set_title(f'{t1} {event_type} Map', fontsize=12, color = "black")




    fig.savefig('./public/analysis/heatmap.png')
  
