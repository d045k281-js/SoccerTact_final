import sys
img = str(sys.argv[1])
def get_images_links(searchTerm):

    import requests
    from bs4 import BeautifulSoup

    searchUrl = "https://www.google.com/search?q={}&site=webhp&tbm=isch".format(searchTerm)
    d = requests.get(searchUrl).text
    soup = BeautifulSoup(d, 'html.parser')

    img_tags = soup.find_all('img')

    imgs_urls = []
    for img in img_tags:
        if img['src'].startswith("http"):
            imgs_urls.append(img['src'])

    return(imgs_urls)
url=get_images_links(img)
print(url[0])
import json
with open('./public/analysis/data.json', 'w') as f:
    json.dump(url[0], f)
