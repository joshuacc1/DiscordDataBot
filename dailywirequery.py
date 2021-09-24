from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import feedparser
from bs4 import BeautifulSoup
from Database.DatabaseManagement import  feedsmanagement
from pymongo import MongoClient
import json

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

def collect_new_daily_wire_articles():
    f = open("MONGODB", 'r')
    info = json.load(f)
    f.close()

    ip = info['hostname']
    port = int(info['port'])

    client = MongoClient(ip, port)
    coll = client.get_database('rssdata').get_collection('rssentries')
    results = list(coll.find({'posted': {'$exists':False}}))
    for result in results:
        coll.update_many({'link':result['link']}, {'$set': {'posted':True}})

    res = [(i['title'],
            i['author'],
            i['link'],
            clearhtml(i['content'][0]['value'])) for i in results]
    return res

def update_database():
    rss = 'https://www.dailywire.com/feeds/rss.xml'
    feed = feedparser.parse(rss)
    fm = feedsmanagement()
    fm.addfeed(feed)

#query_daily_wire('Biden lost to the Taliban',database='file')
#print(query_dailywire_paragraphs('Biden lost to the Taliban',database='file'))