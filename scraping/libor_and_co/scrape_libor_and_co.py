from bs4 import BeautifulSoup
import requests
import sys
sys.path.append('../')
from cocktail_parser import cocktail_parser
import re
import pickle

# build list of individual cocktail urls
libor_list_final = []
for i in range (1,16):
    print('building {}'.format(str(i)))
    url = "https://www.liberandcompany.com/collections/recipes?page=" + str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    libor_list = soup.find_all('script', type = "application/ld+json")
    libor_list = re.findall(r"\"url\": \".*\",", str(libor_list))

    for entry in libor_list:
        entry_url = entry[8:-2]
        libor_list_final.append(entry_url)

# build dataset
dat = {}
i = 0
for url in libor_list_final:
    i += 1
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    recipe = soup.get_text()
    
    # get data elements
    cocktail_name = re.findall("([^/]+$)", url)[0]
    print('number: {} ......... cocktail: {}'.format(str(i), cocktail_name))
    
    try:
        glass = re.findall('(glass:\n\n)(.+)', recipe.lower())[0][1]
    except:
        glass = 'missing'
        
    garnish = re.findall('(garnish:\n\n)(.+)', recipe.lower())[0][1]
    cocktail_recipe, _ = cocktail_parser(recipe)
    
    # get picture
    all_img = soup.find_all('img')
    img_url = []
    for x in all_img:
        try:
            img_url.append(x['data-zoom-src'][2:])
        except:
            pass
    
    # build dictionary for an individual cocktail
    single_dat = {
        'glass': glass,
        'recipe': cocktail_recipe,
        'garnish': garnish,
        'img_url': img_url,
    }
        
    # append to big dictionary
    dat[cocktail_name] = single_dat
    
# pickle
pickle.dump(dat, open("libor_co_dat.p", "wb"))