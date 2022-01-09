from bing_image_downloader import downloader
import os
from random import randrange

# THIS NEEDS TO BE RAN IN /mnt/LIBOR/raw


# need ~150 total images
N_pix_per_query = 30
VAL_PERCENT = 0.2

query_dict = {
    'martini': [
        'vodka martini',
        'dirty martini',
        'martini drink',
        'martini cocktail',
        'martini glass'
    ]
}

try:
    os.mkdir('train')
    os.mkdir('val')
except:
    pass

# downloads generically named files to cwd / martini / dirty martini
for cat, queries in query_dict.items():
    try:
        os.mkdir(os.path.join('train',cat))
        os.mkdir(os.path.join('val',cat))
    except:
        pass
    
    for query in queries:
        downloader.download(query,
                            limit = N_pix_per_query,
                            output_dir = cat,
                            adult_filter_off = False,
                            force_replace = True,
                            timeout = 10)
       
        
        # selects some images for validation
        val_nums = [randrange(0,N_pix_per_query) for x in range(int(N_pix_per_query * VAL_PERCENT))]        
        
        # moves files up a level and adds a prefix
        for i, filename in enumerate(os.listdir(os.path.join(cat,query))):
            if i in val_nums:
                p = 'val'
            else:
                p = 'train'
            os.rename(os.path.join(cat,
                                   query,
                                   filename), 
                      os.path.join(p,
                                   cat,
                                   query.replace(' ', '_') + '_' + filename))
        
        # removes empty dirs
        os.rmdir(os.path.join(cat,query))
    os.rmdir(os.path.join(cat))