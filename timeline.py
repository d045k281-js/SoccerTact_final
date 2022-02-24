import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

#ID for England vs Sweden Womens World Cup
match_id_required = 18245
home_team_required ="Real Madrid"
away_team_required ="Liverpool"

file_name=str(match_id_required)+'.json'

import json
with open('C:/Users/fares/Documents/eecs 582/project/SoccerTact/'+file_name) as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)
    
#get the nested structure into a dataframe 
#store the dataframe in a dictionary with the match id as key (remove '.json' from string)
from pandas.io.json import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])
# gdp_dict = {home_team_required : [],
#                 'Match details': ['total_shots','total_passes','total_corners','total_freekicks','total_offside'],
#                 away_team_required: []}
possession = []

real_data =  df.loc[df['team_name'] == 'Real Madrid'].set_index('id')

new_df = real_data[real_data['location'].notna()]
eventNames = []
minute = []
for i, events in real_data.iterrows():
    if (events['type_name'] == "Shot"):
        outcome=events['shot_outcome_name']
        if outcome  == 'Goal':
            name = 'Goal\n' + events['player_name']
            eventNames.append(name)
            minute.append(events['minute'])
    elif (events['type_name'] =='Substitution'):
        name = 'Out: ' + events['player_name'] +'\nIn: ' + events['substitution_replacement_name']
        eventNames.append(name) 
        minute.append(events['minute'])
    elif (events['type_name'] =='Half Start'):
        eventNames.append('Kick-Off') 
        minute.append(events['minute'])
    elif (events['type_name'] =='Foul Committed'):
        if (events['foul_committed_card_name'] == "Yellow Card"):
            name = 'Yellow Card\n'+ events['player_name']
            eventNames.append(name) 
            minute.append(events['minute'])
        elif (events['foul_committed_card_name'] == "Red Card"):
            name = 'Red Card\n'+ events['player_name']
            eventNames.append(name) 
            minute.append(events['minute'])


print (eventNames)
dates = ['0' , '45', '90']

# # Choose some nice levels
levels = np.tile([-5, 5, -3, 3, -1, 1], int(np.ceil(len(minute)/6)))[:len(minute)]
# print (levels)
# # Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
ax.set(title="Real Madrid")
# plt.xlim(0,90)
markerline, stemline, baseline = ax.stem(minute, levels)

#plt.setp(markerline, mec="k", mfc="w", zorder=3)

# # Shift the markers to the baseline by replacing the y-data by zeros.
#markerline.set_ydata(np.zeros(len(dates)))

# annotate lines
vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
for d, l, r, va in zip(minute, levels, eventNames, vert):
    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                textcoords="offset points", va=va, ha="center")

# # format xaxis with 4 month intervals
# # ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
# # ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
# # plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# # remove y axis and spines
ax.get_yaxis().set_visible(False)
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)

# ax.margins(y=0.1)
plt.show()