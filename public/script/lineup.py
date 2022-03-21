"""
Created on Sun Feb  6 17:08:54 2022
@author: atifsiddiqui
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from pandas import json_normalize
import json
import requests
m_id = sys.argv[1]

to_fetch = m_id+'.json'
l_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/"+to_fetch
l_data = json.loads((requests.get(l_site)).text)

df = json_normalize(l_data, sep = "_").assign(match_id = m_id)
    
away_team_lineup = df.loc[0, 'lineup']
home_team_lineup = df.loc[1, 'lineup']

Homenames = [nm['player_name'] for nm in home_team_lineup]
Awaynames = [nm['player_name'] for nm in away_team_lineup]


json_string = json.dumps(Homenames, ensure_ascii=False)
jsonFile = open("./public/analysis/home_line.json", "w",encoding="utf-8")
jsonFile.write(json_string)
jsonFile.close()


json_string = json.dumps(Awaynames, ensure_ascii=False)
jsonFile = open("./public/analysis/away_line.json", "w", encoding="utf-8")
jsonFile.write(json_string)
jsonFile.close()

