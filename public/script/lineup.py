#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:08:54 2022

@author: atifsiddiqui
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from pandas.io.json import json_normalize
import json

match_id = sys.argv[1]

file_name=str(match_id)+'.json'


with open('/Users/deepak/Documents/SoccerTact/data/lineups/'+file_name) as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)


df = pd.json_normalize(data, sep = "_").assign(match_id = file_name[:-5])
    
away_team_lineup = df.loc[0, 'lineup']
home_team_lineup = df.loc[1, 'lineup']

Homenames = [nm['player_name'] for nm in home_team_lineup]
Awaynames = [nm['player_name'] for nm in away_team_lineup]


json_string = json.dumps(Homenames, ensure_ascii=False)
jsonFile = open("./public/analysis/home_line.json", "w")
jsonFile.write(json_string)
jsonFile.close()


json_string = json.dumps(Awaynames, ensure_ascii=False)
jsonFile = open("./public/analysis/away_line.json", "w")
jsonFile.write(json_string)
jsonFile.close()
