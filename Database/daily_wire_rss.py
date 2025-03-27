from manage_mongo import ManageClient
import feedparser
from pprint import pprint

DATABASE = 'test_rss_data'
COLLECTION = 'test_rss_feeds'

def update_database():
    rss = 'https://www.dailywire.com/feeds/rss.xml'
    feed = feedparser.parse(rss)
    data = []
    for entry in feed['entries']:
        entry['source'] = feed['feed']
        if 'author' in entry and 'title' in entry:
                                # status = db.update_one({'id': entry['id'],
                                #         'author': entry['author'],
                                #        'title': entry['title']},
                                #        {'$set': entry},
                                #            upsert = True)
            data.append({'id':entry['id'],
                         'author':entry['author'],
                         'title':entry['title'],
                         'entry':dict(entry)})
            pprint(data)
        print
        break
            

def addfeed(entries):
    new_articles = []
    updated_articles = []
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        for entry in enteries:
            status = db.update_one({'id': entry['id'],
                                'author': entry['author'],
                                'title': entry['title']},
                                {'$set': entry['entry']},
                                    upsert = True)
            if 'upserted' in status.raw_result:
                new_articles.append(entry)
            elif status.raw_result['nModified'] > 0:
                updated_articles.append(entry)
    return new_articles, updated_articles

update_database()