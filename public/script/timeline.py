import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.ticker import MultipleLocator
#ID for England vs Sweden Womens World Cup
match_id_required = 69299
home_team_required ="Real Madrid"
away_team_required ="Barcelona"

file_name=str(match_id_required)+'.json'

import json
with open('../data/data/events/'+file_name, encoding="utf-8") as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)
    
#get the nested structure into a dataframe 
#store the dataframe in a dictionary with the match id as key (remove '.json' from string)
from pandas.io.json import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])


real_data =  df.loc[df['team_name'] == 'Real Madrid'].set_index('id')

new_df = real_data[real_data['location'].notna()]
eventNames = []
details = []
minute = []
for i, events in real_data.iterrows():
    if (events['type_name'] == "Shot"):
        outcome=events['shot_outcome_name']
        if outcome  == 'Goal':
            details.append(events['player_name'])
            eventNames.append('Goal')
            minute.append(events['minute'])
    elif (events['type_name'] =='Substitution'):
        name = 'Out: ' + events['player_name'] +'\nIn: ' + events['substitution_replacement_name']
        details.append(name) 
        eventNames.append("Substitution")
        minute.append(events['minute'])
    elif (events['type_name'] =='Half Start'):
        details.append("") 
        eventNames.append('Kick-Off') 
        minute.append(events['minute'])
    elif (events['type_name'] =='Foul Committed'):
        if (events['foul_committed_card_name'] == "Yellow Card"):
            details.append(events['player_name']) 
            eventNames.append('Yellow Card') 
            minute.append(events['minute'])
        elif (events['foul_committed_card_name'] == "Red Card"):
            details.append(events['player_name']) 
            eventNames.append('Red Card') 
            minute.append(events['minute'])
    elif(events['type_name']=='Bad Behaviour'):
        if (events['bad_behaviour_card_name'] == "Yellow Card"):
            details.append(events['player_name']) 
            eventNames.append('Yellow Card') 
            minute.append(events['minute'])
        elif (events['bad_behaviour_card_name'] == "Red Card"):
            details.append(events['player_name']) 
            eventNames.append('Red Card') 
            minute.append(events['minute'])


dates = ['0' , '45', '90']

# # Choose some nice levels
levels = np.tile([-5, 5, -3, 3, -1, 1], int(np.ceil(len(minute)/6)))[:len(minute)]
# print (levels)
# # Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
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
    ax.annotate(r+'\n'+d+'\n'+str(m) +"'", xy=(m, l), xytext=(-3, np.sign(l)*4),
                textcoords="offset points", va=va, ha="center")


# # format xaxis with 4 month intervals
ax.get_xaxis().set_major_locator(MultipleLocator(45))
# # ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# # remove y axis and spines
ax.get_yaxis().set_visible(False)
#ax.get_xaxis().set_visible(False)
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)
plt.savefig("timeline.jpg") 
# ax.margins(y=0.1)