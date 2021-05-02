from bing_image_downloader import downloader
import os

# download image
# check type?
# check size
# check if shitty?
# do some math on HD space lol

N_pix_per_query = 30

query_dict = {
    'martini': [
        'martini',
        'dirty martini',
        'gin martini',
        'martini cocktail',
        'martini glass'
    ]
}

for cat, queries in query_dict.items():
    for query in queries:
        downloader.download(query,
                            limit = N_pix_per_query,
                            output_dir = cat,
                            adult_filter_off = True,
                            force_replace = True,
                            timeout = 60)
        
        
# bing downloader enforces some stupid folder structuring that I need to clean up