
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
                #print("TH : " + str(th.text))
                innerText = ''
                #if (th.text == "Position(s)"):
                for elem in td.recursiveChildGenerator():
                        #print("elem: " + str(elem))
                    if isinstance(elem, str):
                            innerText += elem.strip()
                            #print("INNER: " + str(innerText))
                    elif elem.name == 'br':
                            innerText += '\n'
                    #print(innerText)
                info[th.text] = innerText

    #print(json.dumps(info, indent=1))

    Name = info["Full name"].strip('[1]')
    Birth = info["Date of birth"].replace(u'\xa0', u' ')
    DOB = Birth.split("(", 2)[1]
    DOB = DOB.split(")", 2)[0]
    Age = Birth.split("age ", 2)[1]
    Age = Age.split(")", 2)[0]
    He = info["Height"]
    Height = He.split("(",1)[1] 
    hei = Height.split(")", 2)[0].replace(u'\xa0', u' ')
    pos = info['Position(s)']
    try: 
            team = info["Current team"]
    except KeyError: 
            team = "Retired"

    try:        
            num = info["Number"]
    except KeyError:
            num = "-"

    player_info = [Name, DOB, Age, hei, pos, team, num]

    jsonString = json.dumps(player_info)
    with open("./public/ply_analysis/data.json", 'w') as outfile:
        outfile.write(jsonString)
    
