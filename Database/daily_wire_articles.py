# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import feedparser
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
from datetime import datetime

with open('SERVERPARAMS') as f:
    server_params = json.load(f)
    database_info = server_params['databases']['daily_wire']
    DATABASE = database_info['database']
    COLLECTION = database_info['collection']

def query_daily_wire(query,database='mongodb',strength=0.1):
    if database == 'mongodb':
        fm = feedsmanagement()
        data = fm.getfeeds()
        for item in data:
            text=''
            contents = item['content']
            for content in contents:
                text += clearhtml(content['value'])
            item['ptext'] = text
    elif database == 'file':
        with open('dailywirearticles.json') as f:
            data = []
            jsonload = json.load(f)
            for item in jsonload:
                data.append(jsonload[item])
                contents = jsonload[item]['content']
                text = ''
                for content in contents:
                    text += clearhtml(content['value'])
                jsonload[item]['ptext'] = text

    articles = [x['ptext'] for x in data]
    query = [query]
    # f = open('Data/dailywirearticles.csv')
    # articles = list(f.readlines())
    # f.close()

    va = TfidfVectorizer(stop_words='english', analyzer='word')
    va_vec = va.fit_transform(articles)
    vq_vec = va.transform(query)

    cosine_similiarity = cosine_similarity(va_vec,vq_vec)
    enum_cs = enumerate(cosine_similiarity)
    enum_cs = sorted(enum_cs, key=lambda x: x[1], reverse=True)
    res = [(data[enum_cs[i][0]]['title'],
            data[enum_cs[i][0]]['author'],
            data[enum_cs[i][0]]['link'],
            articles[enum_cs[i][0]]) for i in range(len(enum_cs)) if enum_cs[i][1] > strength]
    return res

def query_dailywire_paragraphs(query, database = 'mongodb',strength=0.1):
    if database == 'mongodb':
        fm = feedsmanagement()
        data = fm.getfeeds()
        for item in data:
            text=''
            contents = item['content']
            for content in contents:
                text += clearhtml(content['value'])
            item['ptext'] = text
    elif database == 'file':
        with open('dailywirearticles.json') as f:
            data = []
            jsonload = json.load(f)
            for item in jsonload:
                data.append(jsonload[item])
                contents = jsonload[item]['content']
                text = ''
                for content in contents:
                    text += clearhtml(content['value'])
                jsonload[item]['ptext'] = text
                content = jsonload[item]['content'][0]['value']
                soup = BeautifulSoup(content, 'html.parser')
                jsonload[item]['paragraphs'] = []
                for res in soup.find_all('p'):
                    jsonload[item]['paragraphs'].append(res.text)
    articles=[]
    for item in data:
        articles.extend([(item,x) for x in item['paragraphs']])
    query = [query]
    va = TfidfVectorizer(stop_words='english', analyzer='word')
    va_vec = va.fit_transform([x[1] for x in articles])
    vq_vec = va.transform(query)

    cosine_similiarity = cosine_similarity(va_vec,vq_vec)
    enum_cs = enumerate(cosine_similiarity)
    enum_cs = sorted(enum_cs, key=lambda x: x[1], reverse=True)
    res = [(articles[enum_cs[i][0]][0]['title'],
            articles[enum_cs[i][0]][0]['author'],
            articles[enum_cs[i][0]][0]['link'],
            articles[enum_cs[i][0]][1]) for i in range(len(enum_cs)) if enum_cs[i][1] > strength]
    counts = defaultdict(lambda: 0)
    for r in res:
        counts[r[0]] += 1
    counts = [(key, value) for key, value in sorted(counts.items(), key=lambda item: item[1], reverse=True)]
    result = []
    for count in counts[0:3]:
        if count[1] >= 4:
            for r in res:
                if count[0] == r[0]:
                    result.append(r)
                    break
    return result

def clearhtml(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = ""
    for i in soup.find_all('p'):
        text += i.text
    return text

def daily_wire_rss():
    rss = 'https://www.dailywire.com/feeds/rss.xml'
    feed = feedparser.parse(rss)
    articles = []
    for entry in feed["entries"]:
        for c in entry['content']:
            soup = BeautifulSoup(c['value'], 'html.parser')
            text = ""
            for i in soup.find_all('p'):
                text += i.text
            articles.append((entry['title'], i.text))

def update_database():
    """
    Fetches RSS feeds and updates the database with new and updated feeds.

    Returns:
        dict: A dictionary containing lists of new and updated feeds.
    """
    # Load database parameters
    with open("SERVERPARAMS", 'r') as f:
        server_params = json.load(f)
        info = server_params['mongodb']

    # RSS feed URL
    rss = 'https://www.dailywire.com/feeds/rss.xml'
    feed = feedparser.parse(rss)

    # Connect to MongoDB
    client = MongoClient(info['host'], info['port'])
    database_info = server_params['databases']['daily_wire']
    db = client[database_info['database']][database_info['collection']]

    new_feeds = []
    updated_feeds = []

    # Iterate through RSS feed entries
    for entry in feed['entries']:
        # Prepare the feed data
        feed_data = {
            'id': entry['id'],
            'author': entry.get('author', 'Unknown'),
            'title': entry['title'],
            'link': entry['link'],
            'content': entry.get('content', []),
            'source': feed['feed'],
            'published': entry.get('published', None),
            'updated': entry.get('updated', None)
        }

        # Check if the feed already exists in the database
        existing_feed = db.find_one({'id': entry['id']})

        if existing_feed:
            # Check if the feed has been updated
            if feed_data != existing_feed:
                # Update the existing feed in the database
                db.update_one({'id': entry['id']}, {'$set': feed_data})
                updated_feeds.append(feed_data)
        else:
            # Insert the new feed into the database
            db.insert_one(feed_data)
            new_feeds.append(feed_data)

    # Close the MongoDB connection
    client.close()

    # Reverse the order of the feeds
    new_feeds = list(reversed(new_feeds))
    updated_feeds = list(reversed(updated_feeds))

    # Return the lists of new and updated feeds
    return {'new_feeds': new_feeds, 'updated_feeds': updated_feeds}

if __name__ == "__main__":
    #update_database_date('2021-08-01', '2021-08-31')
    res = update_database()
    for r in res['new_feeds']:
        print(r['title'])