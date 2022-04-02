import sys
import requests
import json
from pandas import json_normalize

def getNumber(m_id, l_data, name):
  df = json_normalize(l_data, sep = "_").assign(match_id = m_id)    
   
  for x in df['lineup']:
      for y in x:
          if y['player_name'] == str(name):
              return(y['jersey_number'])
