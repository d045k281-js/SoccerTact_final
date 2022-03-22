
import requests
import bs4
import json
import sys


def scrapeInfo(player_name):
    text = str(player_name)
    url = 'https://en.wikipedia.org/wiki/' + text
    request_result=requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html")

    #print(soup.prettify())
    tbl = soup.find('div', {'class': 'mw-parser-output'})
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

    #print(json.dumps(info, indent=1))

    Name = info["Full name"].strip('[1]')
    Birth = info["Date of birth"]
    DOB = Birth[12:24] 
    Age = Birth[29:31]
    Height = info["Height"]
    h = Height[-60:9]
    hei = h.replace(u'\xa0', u' ')
    pos = info['Position(s)']
    team = info["Current team"]
    num = info["Number"]

    player_info = [Name, DOB, Age, hei, pos, team, num]

    jsonString = json.dumps(player_info)
    jsonFile = open("./public/ply_analysis/data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close() 

