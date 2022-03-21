
import requests
import bs4
import json
import sys

text= "Lionel Messi"

soup = bs4.BeautifulSoup(text, "html")

#print(soup.prettify())
tbl=soup.find('table', id="datatable_main")
list_of_table_rows = tbl.findAll('tr')
info = {}
for tr in list_of_table_rows:
    th = tr.find("th")
    td = tr.find("td")  
    #for a in tr.find_all('a', href=True):
        #print("Found the URL:", a['href'])
        
    if th is not None and td is not None:
            innerText = ''
            for elem in td.recursiveChildGenerator():
                if isinstance(elem, str):
                    innerText += elem.strip()
                elif elem.name == 'br':
                    innerText += '\n'
            info[th.text] = innerText

print(json.dumps(info, indent=1))

Name = info["Full name"].strip('[1]')
Birth = info["Date of birth"]
DOB = Birth[12:24] 
Age = Birth[29:31]
Height = info["Height"]
hei = Height[8:17]
pos = info['Position(s)']
team = info["Current team"]
num = info["Number"]

player_info = [Name, DOB, Age, hei, pos, team, num]
