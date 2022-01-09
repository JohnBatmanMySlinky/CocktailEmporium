import re


def delete_long_descriptors(recipe):
    recipe_new = []
    for each in recipe:
        longest = max([x.strip().count(' ') for x in each])
        if longest <= 6:
            recipe_new.append(each)
    return recipe_new

def expand_forgotten(recipe, adjectives, noun):
    """
    for recipes when they say 'lemon' but mean 'lemon juice'
    """
    for adjective in adjectives:
        regex_str = rf"{adjective},|{adjective}\n|{adjective}$"
        if re.findall(regex_str, recipe):
            recipe = recipe.replace(adjective, adjective+' '+noun)

    return recipe

def clean_up_silly_stuff(recipe):
    recipe = recipe.replace('oz.', 'oz')

    ##############
    # REGEXERY
    ##############
    # there either are or there aren't measure words
    # remove matches with too many words

    # TODO
    # Regex is currently doing hte below, can I collapse some?
    # # #/#
    # #/#
    # #.##
    # #.#
    # .##
    # .#
    # #
    # can I also collapse w/ and w/o measure words?

    # unicode fractions
    unicode_fraction_dict = {
        r'\u00BC': ' 1/4',
        r'\u00BD': ' 1/2',
        r'\u00BE': ' 3/4',
        r'\u2150': ' 1/7',
        r'\u2151': ' 1/9',
        r'\u2152': ' 1/10',
        r'\u2153': ' 1/3',
        r'\u2154': ' 2/3',
        r'\u2155': ' 1/5',
        r'\u2156': ' 2/5',
        r'\u2157': ' 3/5',
        r'\u2158': ' 4/5',
        r'\u2159': ' 1/6',
        r'\u215A': ' 5/6',
        r'\u215B': ' 1/8',
        r'\u215C': ' 3/8',
        r'\u215D': ' 5/8',
        r'\u215E': ' 7/8',
    }
    for k, v in unicode_fraction_dict.items():
        recipe = re.sub(k, v, recipe)
    recipe = recipe.replace(u'\xa0', ' ')

    return recipe

def cocktail_parser(recipe):
    recipe = recipe.lower()

    # build lists for regex
    end_words = open("../lingo/ingredients.txt", "r").read().strip().split('\n')
    end_words_str = '|'.join(end_words)
    measure_words = open("../lingo/units.txt", "r").read().strip().split('\n')
    measure_words_str = '|'.join(measure_words)

    # converting unicode fractions and other misc clean up of the raw recipe
    recipe = clean_up_silly_stuff(recipe)

    # for cases where we have 'lemon' but not 'lemon juice' or 'simple' but not 'simple syrup' or 'Angostura but not Angostura bitters'
    # does some checks to not end up with 'lemon juice juice'
    forgotten_dict = {
        'syrup': ['simple'],
        'juice': ['lemon', 'lime'],
        'bitters': ['angostura']
    }
    for noun, adjectives in forgotten_dict.items():
        recipe = expand_forgotten(recipe, adjectives, noun)

    # remove anything within ()
    # such as '2 oz (60ml) of booze'
    recipe = re.sub(r'\([^)]*\) ', '', recipe)

    # assume there are measure words
    regex_str = r'([0-9] [0-9]\/[0-9]|[0-9]\/[0-9]|[0-9]\.[0-9][0-9]|[0-9]\.[0-9]|\.[0-9][0-9]|\.[0-9]|[0-9][0-9]|[0-9])(|.+)(' + measure_words_str + r')(.+?)\b(' + end_words_str + r')\b'
    recipe_parsed = re.findall(regex_str, recipe)
    recipe_parsed = delete_long_descriptors(recipe_parsed)

    # assume there ARENT measure words
    regex_str_no_measure_words = r'([0-9] [0-9]\/[0-9]|[0-9]\/[0-9]|[0-9]\.[0-9][0-9]|[0-9]\.[0-9]|\.[0-9][0-9]|\.[0-9]|[0-9][0-9]|[0-9])(|.+)(' + end_words_str + r')'
    recipe_parsed_no_measure = re.findall(regex_str_no_measure_words, recipe)
    recipe_parsed_no_measure = delete_long_descriptors(recipe_parsed_no_measure)

    # no measure version will add duplicate, bad matches
    # remove duplicates from no measure version
    for each in recipe_parsed_no_measure:
        if not any(each[-1] in x for x in recipe_parsed):
            recipe_parsed.append(each)

    ##############
    # Misc Clean Up
    ##############
    # clean up regex results. maybe if regex didn't give me migraines I could make the regex do this.
    recipe_final = []
    for tup in recipe_parsed:
        # strip white spaces
        ls = [x.strip() for x in tup if x != ' ']

        # remove '' 's
        while '' in ls:
            ls.remove('')

        # remove 'of '
        ls = [x.replace('of ','') for x in ls]

        # convert '#/#' fractions
        if ls[0].find('/') > -1 and len(ls[0]) == 3:
            ls[0] = float(ls[0][0]) / float(ls[0][2])

        # convert '# #/#' fractions
        elif ls[0].find('/') > -1 and len(ls[0]) == 5:
            ls[0] = float(ls[0][0]) + float(ls[0][2]) / float(ls[0][4])

        # not a fraction
        else:
            pass

        # first item is always a number, convert to float
        ls[0] = float(ls[0])

        # forcing each line of a ingredient to have 4 items
        ## NUMBER
        ## UNIT
        ## ADJECTIVE
        ## INGREDIENT
        if len(ls) == 4:
            pass
        elif len(ls) == 3 and ls[1] in measure_words:
            ls.insert(2, '')
        elif len(ls) == 3 and ls[1] not in measure_words:
            ls.insert(1, '')
        elif len(ls) == 2:
            ls.insert(1, '')
            ls.insert(1, '')
        else:
            assert len(ls) > 1, 'something went wrong, ingredient in cocktail too short'

        recipe_final.append(ls)

    ##############
    # Garnish
    ##############
    try:
        if 'garnish' in recipe:
            garnish = recipe[:]
            garnish = re.sub(r'[\(\[].*?[\)\]]', '', garnish)
            garnish = re.sub(r'\*', '', garnish)
            garnish = re.findall(r'garnish.+\n', garnish)
            garnish = [x.replace('  ', ' ').strip() for x in garnish][0]
        else:
            garnish = None
    except:
        garnish = None

    return recipe_final, garnish
