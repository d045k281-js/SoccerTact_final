from encodings import utf_8
import os
import sys
import git
import json
from matplotlib.font_manager import json_dump
from pandas import json_normalize


r = git.Repo.clone_from('https://github.com/statsbomb/open-data.git', '/Users/deepak/Documents/SoccerTact_final/public/data')

l_p = '/Users/deepak/Documents/SoccerTact_final/public/data/data/lineups'
f = []

for root, directories, files in os.walk(l_p):
    for filename in files:
        filepath = os.path.join(root, filename)
        f.append(filename) 

fileList = [i.replace(".json","") for i in f]

d_list = []

for id in fileList:
    q = l_p+'/'+id+'.json'
    w = open(q, encoding="utf8")
    l_data = json.load(w)

    #getting the name of the teams
    df = json_normalize(l_data, sep = "_").assign(match_id = id)
    events = df.loc[df['match_id'] == id]
    t1 ='a'
    for i,event in events.iterrows():
        if(t1=='a'):
            t1 = event['team_name']
        else:
            t2 = event['team_name']

    dictionary = {
        "home_team" : t1,
        "away_team" : t2,
        "match_id" : id
    }
    d_list.append(dictionary)

with open("s_d.json", "w", encoding='utf-8') as outfile:
    json.dump(d_list, outfile, ensure_ascii = False)