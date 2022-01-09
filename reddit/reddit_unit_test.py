# This Python file uses the following encoding: utf-8
import sys
from scrape_reddit import scrape_r_cocktails

test_dict = {
    'knej2c': [[1.0, 'oz', 'reposado', 'tequila'],
               [0.75, 'oz', 'smith & cross jamaican', 'rum'],
               [0.5, 'oz', 'velvet', 'falernum'],
               [0.25, 'oz', '', 'mezcal'],
               [0.75, 'oz', 'lime', 'juice'],
               [0.25, 'oz', 'grapefruit', 'juice'],
               [0.25, 'oz', 'cinnamon', 'syrup'],
               [1.0, 'tsp', '', 'grenadine'],
               [1.0, 'dash', 'angostura', 'bitters']],
    'ku610i': [[0.75, '', 'jamaican', 'rum'],
               [0.75, '', '', 'galliano'],
               [0.75, '', '', 'suze'],
               [0.75, '', 'lemon', 'juice']],
    'kuhlkq': [[2.0, 'oz', '', 'gin'],
               [1.0, 'oz', '', 'cointreau'],
               [0.75, 'oz', 'freshly squeezed lemon', 'juice'],
               [0.5, 'oz', '', 'campari']],
    'kuy98o': [[0.75, 'oz', '', 'yellow chartreuse'],
               [0.75, '', '', 'mezcal'],
               [0.75, '', '', 'aperol'],
               [0.5, '', '', 'green chartreuse'],
               [0.25, '', 'simple', 'syrup'],
               [0.75, '', 'fresh lime', 'juice']],
    'kup5c3': [[2.0, 'oz', "dewar’s 12 blended", 'scotch'],
               [0.75, 'oz', 'honey&ginger', 'syrup'],
               [0.75, 'oz', 'lemon', 'juice'],
               [0.5, 'oz', 'lagavulin 16 islay single malt', 'whiskey']],
    'l1aodj': [[1.5, 'oz', 'rye', 'whiskey'],
               [0.75, 'oz', '', 'campari'],
               [1.5, 'oz', 'pineapple', 'juice'],
               [1.0, 'oz', 'freshly squeezed lemon', 'juice'],
               [0.75, 'oz', 'passion fruit', 'syrup']],
    'l1ye7f': [[1.5, 'oz', '', 'gin'],
               [0.25, 'oz', '', 'yellow chartreuse'],
               [0.75, 'oz', 'elderflower', 'liqueur'],
               [0.75, 'oz', 'lemon', 'juice'],
               [1.0, '', '', 'strawberry']],
    'kwtn6f': [[2.0, 'oz', '', 'gin'],
               [0.5, 'oz', '', 'st. germain'],
               [0.5, 'oz', 'mint simple', 'syrup'],
               [0.5, 'oz', 'lemon', 'juice'],
               [5.0, '', 'mint', 'leaves'],
               [5.0, '', 'peach', 'slices']],
    'kpsih3': [[30.0, 'ml', 'bulleit rye', 'whiskey'],
               [30.0, 'ml', 'hennessy', 'cognac'],
               [30.0, 'ml', '', 'carpano antica formula'],
               [5.0, 'ml', 'or barspoon d.o.m.', 'bénédictine'],
               [3.0, 'dashes', 'each angostura and peychaud’s', 'bitters']],
    'l8qdrt': [[2.0, 'oz', "ford's", 'gin'],
               [0.5, 'oz', '', 'vermouth'],
               [0.5, 'tsp', 'champagne', 'vinegar'],
               [2.0, 'dashes', 'orange', 'bitters'],
               [1.0, '', 'lemon', 'peel']],
    'ldm5to' : [[1.5, 'oz', 'blanco', 'tequila'],
                [1.0, 'oz', 'lime', 'juice'],
                [0.75, 'oz', 'simple', 'syrup'],
                [0.5, 'oz', 'red', 'wine']]
}

for k,v in test_dict.items():
    test = scrape_r_cocktails(sys.argv[1], k, 'a', 'a')['recipe_final']
    if test == v:
        print(k + ' worked')
    else:
        print(test)
        print(k + ' DIDNT WORK')


