#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 00:48:06 2022

@author: atifsiddiqui
"""


from hashlib import blake2b
from turtle import color
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

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
from mplsoccer import Pitch, VerticalPitch, FontManager
from matplotlib.colors import to_rgba



def generate_pass(m_id,t1,t2,e_data,l_data):
    
    pitch = Pitch(pitch_type='statsbomb',axis=True, line_zorder=2, line_color='#c7d5cc', pitch_color='#22312b')  # showing axis labels is optional
    bins = (6, 4)
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312b')
    
    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)  
    t1_data =  df.loc[df['team_name'] == t1].set_index('id')
    t2_data =  df.loc[df['team_name'] == t2].set_index('id')

    t1_pass = t1_data.loc[t1_data['type_name'] == 'Pass']
    t2_pass = t1_data.loc[t1_data['type_name'] == 'Pass']
   
    
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
    hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='Reds')
# plot the pass flow map with a single color ('black') and length of the arrow (5)
    fm = pitch.flow(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y,
                color='black', arrow_type='same',
                arrow_length=5, bins=bins, ax=ax)
    #ax.set_title(f'{t1} pass flow map VS {t2}', fontsize=12, color = "red")
    fig.savefig('./public/analysis/t1pass.png', bbox_inches = 'tight')


    for i, event in t2_pass.iterrows():
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
    hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='Reds')
# plot the pass flow map with a single color ('black') and length of the arrow (5)
    fm = pitch.flow(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y,
                color='black', arrow_type='same',
                arrow_length=5, bins=bins, ax=ax)
    # ax.set_title(f'{t2} pass flow map vs {t1}', fontsize=12, color = "red")
    fig.savefig('./public/analysis/t2pass.png', bbox_inches = 'tight')


def passing_network(m_id,t1,t2,e_data,l_data):
   
    path_eff = [path_effects.Stroke(linewidth=1.5, foreground='black'),
            path_effects.Normal()]

    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    
    t1_data =  df.loc[df['team_name'] == t1].set_index('id')
    t2_data = df.loc[df['team_name'] == t2].set_index('id')
    #print(t1_data.head())
    pass_raw = t1_data[t1_data.type_name == 'Pass']
    
    pass_raw = pass_raw.iloc[:, :33]
    #print(pass_raw.head())
    
    # getting number of passes 
    pass_number_raw = pass_raw[['timestamp', 'duration', 'team_name', 'player_name', 'pass_recipient_name']]
    pass_number_raw['pair'] = pass_number_raw.player_name + pass_number_raw.pass_recipient_name
    pass_count = pass_number_raw.groupby(['team_name', 'pair']).count().reset_index()
    pass_count = pass_count[['pair', 'timestamp']]
    pass_count.columns = ['pair', 'number_pass']
    
    #getting average position 
    avg_loc_df = pass_raw[['team_name', 'player_name', 'location']]

    avg_loc_df['pos_x'] = avg_loc_df.location.apply(lambda x: x[0])
    avg_loc_df['pos_y'] = avg_loc_df.location.apply(lambda x: x[1])

    avg_loc_df = avg_loc_df.drop('location', axis=1)

    avg_loc_df = avg_loc_df.groupby(['team_name','player_name']).agg({'pos_x': np.mean, 'pos_y': np.mean}).reset_index()

    #print(avg_loc_df)
    
    pass_merge = pass_number_raw.merge(pass_count, on='pair')
    pass_merge = pass_merge[['team_name', 'player_name', 'pass_recipient_name', 'number_pass']]
    pass_merge = pass_merge.drop_duplicates()
    
    avg_loc_df = avg_loc_df[['player_name', 'pos_x', 'pos_y']]

    pass_cleaned = pass_merge.merge(avg_loc_df, on='player_name')
    pass_cleaned.rename({'pos_x': 'pos_x_start', 'pos_y': 'pos_y_start'}, axis='columns', inplace=True)

    pass_cleaned = pass_cleaned.merge(avg_loc_df, left_on='pass_recipient_name', right_on='player_name', suffixes=['', '_end'])
    pass_cleaned.rename({'pos_x': 'pos_x_end', 'pos_y': 'pos_y_end'}, axis='columns', inplace=True)

    pass_cleaned = pass_cleaned.drop(['player_name_end'], axis=1)
    
    #Retrieve 11 most minute-playerd players
    player_df = df[df.team_name == t1].groupby('player_name').agg({'minute': [min, max]}).reset_index()
    player_df = pd.concat([player_df['player_name'], player_df['minute']], axis=1)
    player_df['minutes_played'] = player_df['max'] - player_df['min']
    player_df = player_df.sort_values('minutes_played', ascending=False)
    #print(player_df)
    player_names = player_df.player_name[:11].tolist()

    pass_team = pass_cleaned[pass_cleaned.player_name.isin(player_names)]
    pass_team = pass_team[pass_team.pass_recipient_name.isin(player_names)]

    #print(pass_team.shape)
    #print(pass_team.head())
    
    #build network 
    pass_team['width'] = pass_team['number_pass'] / pass_team['number_pass'].max()
    #print(pass_team.head())
    
    MIN_TRANSPARENCY = 0.3
    color = np.array(to_rgba('white'))
    color = np.tile(color, (len(pass_team), 1))
    c_transparency = pass_team.number_pass / pass_team.number_pass.max()
    c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
    color[:, 3] = c_transparency
    
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0, axis=False, 
                      title_space=0, grid_height=0.82, endnote_height=0.05)

    fig.set_facecolor("#22312b")

    pass_lines = pitch.lines(pass_team.pos_x_start, pass_team.pos_y_start,
                         pass_team.pos_x_end, pass_team.pos_y_end, lw=pass_team.width+0.5,
                         color=color, zorder=1, ax=axs['pitch'])

    pass_nodes = pitch.scatter(pass_team.pos_x_start, pass_team.pos_y_start, s=450,
                           color='red', edgecolors='black', linewidth=1, alpha=1, ax=axs['pitch'])

    for index, row in pass_team.iterrows():
        pitch.annotate(row.player_name, xy=(row.pos_x_start-3, row.pos_y_start-3), c='white', va='center',
                   ha='center', size=12, ax=axs['pitch'])
    
# endnote /title
    axs['endnote'].text(1, 0.5, '@MixtureModels', color='#c7d5cc',
                    va='center', ha='right', fontsize=15)

    axs['endnote'].text(0.5, 0.9, 'Attacking Direction', va='center', ha='center', color='#c7d5cc', fontsize=12)
    axs['endnote'].arrow(0.4, 0.6, 0.2, 0, head_width=0.25, head_length=0.025, ec='w', fc='w')
    axs['endnote'].set_xlim(0, 1)
    axs['endnote'].set_ylim(0, 1)

    # axs['title'].text(0.5, 0.7, f'{t1} Passing Network VS {t2}', color='#c7d5cc',
    #               va='center', ha='center', fontsize=30)
    fig.savefig("./public/analysis/t1pn.png", bbox_inches = 'tight')


    t2_data = df.loc[df['team_name'] == t2].set_index('id')
    #print(t1_data.head())
    pass_raw = t2_data[t2_data.type_name == 'Pass']
    
    pass_raw = pass_raw.iloc[:, :33]
    #print(pass_raw.head())
    
    # getting number of passes 
    pass_number_raw = pass_raw[['timestamp', 'duration', 'team_name', 'player_name', 'pass_recipient_name']]
    pass_number_raw['pair'] = pass_number_raw.player_name + pass_number_raw.pass_recipient_name
    pass_count = pass_number_raw.groupby(['team_name', 'pair']).count().reset_index()
    pass_count = pass_count[['pair', 'timestamp']]
    pass_count.columns = ['pair', 'number_pass']
    
    #getting average position 
    avg_loc_df = pass_raw[['team_name', 'player_name', 'location']]

    avg_loc_df['pos_x'] = avg_loc_df.location.apply(lambda x: x[0])
    avg_loc_df['pos_y'] = avg_loc_df.location.apply(lambda x: x[1])

    avg_loc_df = avg_loc_df.drop('location', axis=1)

    avg_loc_df = avg_loc_df.groupby(['team_name','player_name']).agg({'pos_x': np.mean, 'pos_y': np.mean}).reset_index()

    #print(avg_loc_df)
    
    pass_merge = pass_number_raw.merge(pass_count, on='pair')
    pass_merge = pass_merge[['team_name', 'player_name', 'pass_recipient_name', 'number_pass']]
    pass_merge = pass_merge.drop_duplicates()
    
    avg_loc_df = avg_loc_df[['player_name', 'pos_x', 'pos_y']]

    pass_cleaned = pass_merge.merge(avg_loc_df, on='player_name')
    pass_cleaned.rename({'pos_x': 'pos_x_start', 'pos_y': 'pos_y_start'}, axis='columns', inplace=True)

    pass_cleaned = pass_cleaned.merge(avg_loc_df, left_on='pass_recipient_name', right_on='player_name', suffixes=['', '_end'])
    pass_cleaned.rename({'pos_x': 'pos_x_end', 'pos_y': 'pos_y_end'}, axis='columns', inplace=True)

    pass_cleaned = pass_cleaned.drop(['player_name_end'], axis=1)
    
    #Retrieve 11 most minute-playerd players
    player_df = df[df.team_name == t2].groupby('player_name').agg({'minute': [min, max]}).reset_index()
    player_df = pd.concat([player_df['player_name'], player_df['minute']], axis=1)
    player_df['minutes_played'] = player_df['max'] - player_df['min']
    player_df = player_df.sort_values('minutes_played', ascending=False)
    #print(player_df)
    player_names = player_df.player_name[:11].tolist()

    pass_team = pass_cleaned[pass_cleaned.player_name.isin(player_names)]
    pass_team = pass_team[pass_team.pass_recipient_name.isin(player_names)]

    #print(pass_team.shape)
    #print(pass_team.head())
    
    #build network 
    pass_team['width'] = pass_team['number_pass'] / pass_team['number_pass'].max()
    #print(pass_team.head())
    
    MIN_TRANSPARENCY = 0.3
    color = np.array(to_rgba('white'))
    color = np.tile(color, (len(pass_team), 1))
    c_transparency = pass_team.number_pass / pass_team.number_pass.max()
    c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
    color[:, 3] = c_transparency
    
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0, axis=False, 
                      title_space=0, grid_height=0.82, endnote_height=0.05)

    fig.set_facecolor("#22312b")

    pass_lines = pitch.lines(pass_team.pos_x_start, pass_team.pos_y_start,
                         pass_team.pos_x_end, pass_team.pos_y_end, lw=pass_team.width+0.5,
                         color=color, zorder=1, ax=axs['pitch'])

    pass_nodes = pitch.scatter(pass_team.pos_x_start, pass_team.pos_y_start, s=450,
                           color='red', edgecolors='black', linewidth=1, alpha=1, ax=axs['pitch'])

    for index, row in pass_team.iterrows():
        pitch.annotate(row.player_name, xy=(row.pos_x_start-3, row.pos_y_start-3), c='white', va='center',
                   ha='center', size=12, ax=axs['pitch'])
    
# endnote /title
    axs['endnote'].text(1, 0.5, '@MixtureModels', color='#c7d5cc',
                    va='center', ha='right', fontsize=15)

    axs['endnote'].text(0.5, 0.9, 'Attacking Direction', va='center', ha='center', color='#c7d5cc', fontsize=12)
    axs['endnote'].arrow(0.4, 0.6, 0.2, 0, head_width=0.25, head_length=0.025, ec='w', fc='w')
    axs['endnote'].set_xlim(0, 1)
    axs['endnote'].set_ylim(0, 1)

    # axs['title'].text(0.5, 0.7, f'{t2} Passing Network VS {t1}', color='#c7d5cc',
    #               va='center', ha='center', fontsize=30)
    fig.savefig('./public/analysis/t2_PN.png', bbox_inches = 'tight')
    
