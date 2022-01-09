import wget
import urllib
import json

with urllib.request.urlopen('https://www.thecocktaildb.com/api/json/v1/1/list.php?g=list') as url:
    glass_dict = json.loads(url.read().decode())
print(glass_dict)



