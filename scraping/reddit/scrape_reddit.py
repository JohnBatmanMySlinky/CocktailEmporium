import sys
sys.path.append('../')
from cocktail_parser import cocktail_parser
import configparser
import praw

def get_post_from_reddit(machine_name, url_id):
    if machine_name == 'VM':
        secrets_dir = '/home/jmyslinski/JOHNS_CONFIG_FILE_NO_TOUCH/config.John'
    elif machine_name == 'John':
        secrets_dir = '/Users/johnmyslinski/Documents/SECRETS/config.John'
    else:
        print('options are John or VM')
        assert 5 == 6

    config = configparser.ConfigParser()
    config.read(secrets_dir)
    reddit = praw.Reddit(
        user_agent=config['REDDIT_API']['user_agent'],
        client_id=config['REDDIT_API']['client_id'],
        client_secret=config['REDDIT_API']['client_secret']
    )

    post = reddit.submission(id=url_id)

    return (post)


def scrape_r_cocktails(machine, url_id, drink_name, drink_category):
    # get submission
    submission = get_post_from_reddit(machine, url_id)

    # get everything out of submission
    submission_url = None
    recipe = None
    author = None
    recipe_final = None
    garnish = None
    score = None

    # get post upvotes
    score = submission.score

    # Get image url
    submission_url = submission.url

    # get recipe and author
    for top_level_comment in submission.comments:
        if submission.author == top_level_comment.author:
            author = str(submission.author)
            recipe = top_level_comment.body.lower()

    # parse recipe to get recipe_fianl and garnish
    recipe_final, garnish = cocktail_parser(recipe)

    # building dict to return
    return_dict = {
        'author': author,
        'url_id': url_id,
        'submission_url': submission_url,
        'score': score,
        'drink_name': drink_name,
        'drink_category': drink_category,
        'recipe_final': recipe_final,
        'garnish': garnish
    }

    return return_dict


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('wrong # args')
        print('sample CLI call below')
        print('python scrape_r_cocktails.py John/VM reddit_url_id cocktailname cocktailcategory')
    else:
        machine = sys.argv[1]
        url_id = sys.argv[2]
        drink_name = sys.argv[3]
        drink_category = sys.argv[4]

        print(scrape_r_cocktails(machine, url_id, drink_name, drink_category))

