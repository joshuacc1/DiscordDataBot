from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import feedparser
from bs4 import BeautifulSoup
from Database.DatabaseManagement import  feedsmanagement

def query_daily_wire(query):
    fm = feedsmanagement()
    data = fm.getfeeds()
    for item in data:
        text=''
        contents = item['content']
        for content in contents:
            text += clearhtml(content['value'])
        item['ptext'] = text
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
            articles[enum_cs[i][0]]) for i in range(len(enum_cs)) if enum_cs[i][1] > 0.1]
    return res

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

query_daily_wire('Biden lost to the Taliban')