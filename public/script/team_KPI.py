#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 13:03:53 2022

@author: 
"""

#Function to draw the pitch
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import dataframe_image as dfi

#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

#ID for England vs Sweden Womens World Cup
match_id_required = 18245
home_team_required ="Real Madrid"
away_team_required ="Liverpool"

file_name=str(match_id_required)+'.json'

import json
with open('C:/Users/fares/OneDrive/Documentos/eecs 582/project/SoccerTact/'+file_name) as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)
    
#get the nested structure into a dataframe 
#store the dataframe in a dictionary with the match id as key (remove '.json' from string)
from pandas.io.json import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])
gdp_dict = {home_team_required : [],
                'Match details': ['total_shots','total_passes','total_corners','total_freekicks','total_offside'],
                away_team_required: []}
possession = []
Liv_data =  df.loc[df['team_name'] == 'Liverpool'].set_index('id')
real_data =  df.loc[df['team_name'] == 'Real Madrid'].set_index('id')

new_df = real_data[real_data['location'].notna()]

def RealteamKPI():
    
    total_shots = 0
    total_passes = 0
    shots_from_penalty_area = 0; 
    penalty_box_entry = 0; 
    actions_PB = 0
    total_corners = 0
    total_freekicks = 0
    duration = 0
    total_offside = 0
    
    # for i, events in new_df.iterrows():
    #      x = events['location'][0]
    #      y = events['location'][1]
   
    #      if(x > 102.0 and (y > 18.0 and y < 62.0)): 
    #         penalty_box_entry = penalty_box_entry + 1
            
            
    #         if (events['type_name'] == 'Shot'):
    #             shots_from_penalty_area = shots_from_penalty_area + 1
                
    
    for i, events in real_data.iterrows():
        if (not pd.isna(events['duration'])):
            duration+=events['duration']
            
        if (events['type_name'] == "Shot"):
            total_shots = total_shots + 1
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
            
    gdp_dict[home_team_required].extend([int(total_shots),total_passes,total_corners,total_freekicks,total_offside]) 
    # print("=================")
    # print("Real Madrid Stats")
    # print("Total Shots " + str(total_shots))
    # print("Total Passes " + str(total_passes))
    # print("Penalty Box Entries " + str(penalty_box_entry))
    # print("Shots from penalty area " + str(shots_from_penalty_area))
    # print("Total Corners " + str(total_corners))
    # print("Total Free Kicks " + str(total_freekicks))
    # print("Total Free Kicks " + str(duration))
    # print("=================")

def LivteamKPI():
    
    total_shots = 0
    total_passes = 0
    shots_from_penalty_area = 0; 
    penalty_box_entry = 0; 
    actions_PB = 0
    total_corners = 0
    total_freekicks = 0
    duration = 0
    total_offside = 0
    
    # for i, events in new_df.iterrows():
    #      x = events['location'][0]
    #      y = events['location'][1]
   
    #      if(x < 18 and (y > 18.0 and y < 62.0)): 
    #         penalty_box_entry = penalty_box_entry + 1
    #         if (events['type_name'] == 'Shot'):
    #             shots_from_penalty_area = shots_from_penalty_area + 1
                
    for i, events in Liv_data.iterrows():
        if (not pd.isna(events['duration'])):
            duration+=events['duration']
        if (events['type_name'] == "Shot"):
            total_shots = total_shots + 1
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
    gdp_dict[away_team_required].extend([int(total_shots),total_passes,total_corners,total_freekicks, total_offside])
    possession.append(duration)
    # print("=================")
    # print("Liverpool Stats")
    # print("Total Shots " + str(total_shots))
    # print("Total Passes " + str(total_passes))
    # print("Penalty Box Entries " + str(penalty_box_entry))
    # print("Shots from penalty area " + str(shots_from_penalty_area))
    # print("Total Corners " + str(total_corners))
    # print("Total Free Kicks " + str(total_freekicks))
    # print("Total Free Kicks " + str(duration))
    # print("=================")

RealteamKPI()    
LivteamKPI()
totalPossession = sum(possession) 
homePossession = int((possession[0]/totalPossession)*100)
awayPossession = 100 - homePossession
gdp_dict[away_team_required].insert(0,awayPossession)
gdp_dict[home_team_required].insert(0,homePossession)
gdp_dict['Match details'].insert(0,"possession")
data = pd.DataFrame(gdp_dict)
data = data. set_index([ home_team_required ,'Match details', away_team_required])
dfi.export(data, 'dataframe.png')