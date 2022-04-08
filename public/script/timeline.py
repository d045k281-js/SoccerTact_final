from turtle import color
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from pandas import json_normalize
from PIL import Image
from matplotlib.ticker import MultipleLocator
from pyparsing import col
from Number import getNumber

def generate_timeline(m_id, t1, e_data, l_data, image):
    df = json_normalize(e_data, sep = "_").assign(match_id = m_id)    
    
    t1_data =  df.loc[df['team_name'] == t1].set_index('id')

    # new_df = t1_data[t1_data['location'].notna()]
    eventNames = []
    details = []
    minute = []
    for i, events in t1_data.iterrows():
        if (events['type_name'] == "Shot"):
            outcome=events['shot_outcome_name']
            if outcome  == 'Goal':
                details.append(getNumber(m_id,l_data,events['player_name']))
                eventNames.append('Goal')
                minute.append(events['minute'])
        elif (events['type_name'] =='Substitution'):
            name = 'Out: ' + str(getNumber(m_id,l_data,events['player_name'])) +'\nIn: ' + str(getNumber(m_id,l_data,events['substitution_replacement_name']))
            details.append(name) 
            eventNames.append("Substitution")
            minute.append(events['minute'])
        elif (events['type_name'] =='Half Start'):
            details.append("") 
            eventNames.append('Kick-Off') 
            minute.append(events['minute'])
        elif (events['type_name'] =='Foul Committed'):
            if (events['foul_committed_card_name'] == "Yellow Card"):
                details.append(getNumber(m_id,l_data,events['player_name']))
                eventNames.append('Yellow Card') 
                minute.append(events['minute'])
            elif (events['foul_committed_card_name'] == "Red Card"):
                details.append(getNumber(m_id,l_data,events['player_name'])) 
                eventNames.append('Red Card') 
                minute.append(events['minute'])
        elif(events['type_name']=='Bad Behaviour'):
            if (events['bad_behaviour_card_name'] == "Yellow Card"):
                details.append(getNumber(m_id,l_data,events['player_name'])) 
                eventNames.append('Yellow Card') 
                minute.append(events['minute'])
            elif (events['bad_behaviour_card_name'] == "Red Card"):
                details.append(getNumber(m_id,l_data,events['player_name'])) 
                eventNames.append('Red Card') 
                minute.append(events['minute'])


    dates = ['0' , '45', '90']

    # # Choose some nice levels
    levels = np.tile([-1,1], int(np.ceil(len(minute)/2)))[:len(minute)]
    print (levels)
    # # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(10, 6),  constrained_layout=True)
    ax.set_facecolor("white")
    # ax.set(title="Real Madrid")
    plt.ylim(-7,7)
    markerline, stemline, baseline = ax.stem(minute, levels)

    #plt.setp(markerline, mec="k", mfc="w", zorder=3)

    # # Shift the markers to the baseline by replacing the y-data by zeros.
    #markerline.set_ydata(np.zeros(len(dates)))

    # annotate lines
    sb = plt.imread('../images/soccer-ball.png') 
    goal = OffsetImage(sb, zoom=0.04)
    goal.image.axes = ax
    ko = plt.imread('../images/kickoff.png') 
    kick =  OffsetImage(ko, zoom=0.03)
    kick.image.axes = ax
    s = plt.imread('../images/substitution.jpg') 
    sub =  OffsetImage(s, zoom=0.03)
    sub.image.axes = ax
    yc = plt.imread('../images/Yellowcard.png') 
    yellow =  OffsetImage(yc, zoom=0.01)
    yellow.image.axes = ax
    rc = plt.imread('../images/Redcard.png') 
    red =  OffsetImage(rc, zoom=0.01)
    red.image.axes = ax

    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for d, m, l, r, va in zip(details, minute, levels, eventNames, vert):
        if(r == "Goal"):
            ab = AnnotationBbox(goal, (m,l), xybox=(0, np.sign(l)*-9),xycoords='data',
                        boxcoords="offset points",
                        pad=0.5) 
        elif (r == "Kick-Off"):
            ab = AnnotationBbox(kick, (m,l), xybox=(0, np.sign(l)*-9),xycoords='data',
                        boxcoords="offset points",
                        pad=0.5) 
        elif (r == "Substitution"):
            ab = AnnotationBbox(sub, (m,l), xybox=(0, np.sign(l)*-9),xycoords='data',
                        boxcoords="offset points",
                        pad=0.5) 
        elif (r == "Yellow Card"):
            ab = AnnotationBbox(yellow, (m,l), xybox=(0, np.sign(l)*-9),xycoords='data',
                        boxcoords="offset points",
                        pad=0.5) 
        elif (r == "Red Card"):
            ab = AnnotationBbox(red, (m,l), xybox=(0, np.sign(l)*-9),xycoords='data',
                        boxcoords="offset points",
                        pad=0.5) 
        # newax = fig.add_axes([d/100,l/10,0.2,0.2], zorder=1)
        # newax.imshow(im)
        ax.add_artist(ab)
        ax.annotate(str(m) +"'\n" + str(d), xy=(m, 0), xytext=(-3, np.sign(l)*40),
                    textcoords="offset points", va=va, ha="center", color="black")


    # # format xaxis with 4 month intervals
    ax.get_xaxis().set_major_locator(MultipleLocator(45))
    # # ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # # remove y axis and spines
    ax.get_yaxis().set_visible(False)
   
    ax.get_xaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)
    plt.savefig(image +'_timeline.png') 
import requests
import json
e_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/18245.json"
e_data = json.loads((requests.get(e_site)).text)
l_site = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/18245.json"
l_data = json.loads((requests.get(l_site)).text, encoding="utf-8")

generate_timeline("7545", 'Real Madrid', e_data, l_data ,"t1")

    # img = Image.open('t1_timeline.png')
    # img = img.convert("RGBA")
    # datas = img.getdata()

    # newData = []
    # for item in datas:
    #     if item[0] == 255 and item[1] == 255 and item[2] == 255:
    #         newData.append((255, 255, 255, 0))
    #     else:
    #         if item[0] > 150:
    #             newData.append((0, 0, 0, 255))
    #         else:
    #             newData.append(item)
    #             print(item)


    # img.putdata(newData)
    # img.save("timeline.png", "PNG")