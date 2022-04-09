import sys
import requests
import json
import matplotlib.pyplot as plt
from pandas import json_normalize
from mplsoccer import Pitch, VerticalPitch, FontManager
from mplsoccer.statsbomb import read_event, EVENT_SLUG

def lineup(m_id,t1, l_data):
    posToCoord = {
        '1' : [5,40],
        '2' : [13,67],
        '3' : [13,54],
        '4' : [13,40],
        '5' : [13,26],
        '6' : [13,13],
        '7' : [20,67],
        '8' : [20,13],
        '9' : [45,54],
        '10' : [45,40],
        '11' : [45,26],
        '12' : [60,67],
        '13' : [60,54],
        '14' : [60,40],
        '15' : [60,26],
        '16' : [60,13],
        '17' : [107,67],
        '18' : [75,54],
        '19' : [75,40],
        '20' : [75,26],
        '21' : [107,13],
        '22' : [107,54],
        '23' : [107,40],
        '24' : [107,26],
        '25' : [97,40],

    }
    
    pitch = Pitch(half = False, pitch_type='statsbomb',pitch_color='grass', line_color='white', stripe=True)  # showing axis labels is optional
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=False, tight_layout=True) 
    df = json_normalize(l_data, sep = "_").assign(match_id = m_id)  
    t1_data =  df.loc[df['team_name'] == t1].set_index('team_id')
    for x in t1_data['lineup']:
        #print(df['team_name'])
        for y in x:
            for variable in y['positions']:
                if variable['start_reason'] == "Starting XI":
                    sc1 = pitch.scatter(posToCoord[str(variable['position_id'])][0], posToCoord[str(variable['position_id'])][1]-2,
                    # size varies between 100 and 1900 (points squared)
                    s=1550,
                    edgecolors='#606060',  # give the markers a charcoal border
                    c='#FFFFFF',  # no facecolor for the markers
                    # for other markers types see: https://matplotlib.org/api/markers_api.html
                    marker='o',
                    ax=ax)
                    
                    annotation = ax.annotate(str(y['jersey_number']),(posToCoord[str(variable['position_id'])][0],
                    posToCoord[str(variable['position_id'])][1]), fontsize=30, ha='center')
                    #ax2 = add_image(image, fig, left=0.054, bottom=0.84, width=0.08, interpolation='hanning')
    
    fig.savefig('lineup.png', bbox_inches = 'tight')
import requests
import json
l_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/18245.json"
l_data = json.loads((requests.get(l_site)).text, encoding="utf-8")
lineup('18245','Real Madrid', l_data)