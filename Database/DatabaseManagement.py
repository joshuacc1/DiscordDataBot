from pymongo import MongoClient
from bs4 import BeautifulSoup
from bs4.element import Comment
from requests import request
import json
import os
from discord.message import Message

class datalink:
    def __init__(self,databasename, databasecollection):
        self.databasename = databasename
        self.databasecollection = databasecollection
        info = json.load(open("MONGODB"))
        self.client = MongoClient(info['hostname'],info['port'])

    def __enter__(self):
        return self.client.get_database(self.databasename).get_collection(self.databasecollection)

    def __exit__(self, type, value, traceback):
        self.client.close()

class messagesmanagement:
    def __init__(self):
        self.database = 'serverdata'
        self.collection = 'messages'

    def addmessage(self, message: Message):

        if message.reference:
            refmessdict = {'message_id': message.reference.message_id,
                           'channel_id': message.reference.channel_id,
                           'guild_id': message.reference.guild_id}
            if message.reference.resolved:
                refmessdict['reply_message'] = message.reference.resolved.content
        else:
            refmessdict = {}
        with datalink(self.database, self.collection) as db:
            db.insert_one({'message_id': message.id,
                           'author': str(message.author),
                           'message': message.content,
                           'guild': str(message.guild),
                           'channel': str(message.channel),
                           **refmessdict})

    def getmessage(self, in_message: str = ''):
        with datalink(self.database,self.collection) as db:
            if in_message:
                return list(db.find({'message':{'$regex': ''.join(["*.",in_message,".*"])}}))
            else:
                return list(db.find({}))

class linksmanagement:
    def __init__(self):
        self.database = datalink('rssdata','rsslinks')

    def addlink(self,category,link, tags=None):
        with self.database as db:
            db.insert_one({'category':category,
                           'tags':tags,
                           'link':link})

    def removelink(self, category=None, link=None):
        with self.database as db:
            finddict = {}
            if category:
                finddict['category'] = category
            if link:
                finddict['link'] = link
            db.delete_many(finddict)

    def getlinks(self, category=None):
        with self.database as db:
            if category:
                results = db.find({'category': category})
            else:
                results = db.find({})

            return [doc for doc in results]


    def printlinks(self):
        with self.database as db:
            for record in db.find({}):
                print(record.get('category') + ': ' + record.get('link').replace('\n',''))

class feedsmanagement:
    def __init__(self):
        self.database = datalink('rssdata', 'rssentries')

    def addfeed(self, feed):
        new_articles = []
        updated_articles = []
        with self.database as db:
            for entry in feed['entries']:
                entry['source'] = feed['feed']
                if 'author' in entry and 'title' in entry:
                    status = db.update_one({'id': entry['id'],
                                        'author': entry['author'],
                                       'title': entry['title']},
                                       {'$set': entry},
                                           upsert = True)
                    if 'upserted' in status.raw_result:
                        new_articles.append(entry)
                    elif status.raw_result['nModified'] > 0:
                        updated_articles.append(entry)
        return new_articles, updated_articles


    def getfeeds(self, category=None):
        _filter = {}
        if category:
            _filter['acategory'] = category
        with self.database as db:
            return [x for x in db.find(_filter)]

    def updateHTMLtexts(self):
        with self.database as db:
            for entry in db.find({}):
                link = entry['link']
                if not 'htmltext' in entry:
                    htmltext = self.getHTMLlinktext(link)
                    db.update({'author': entry['author'], 'title': entry['title']}, {'$set':{'htmltext': htmltext}})


    def getHTMLlinktext(self, link, sensitivity=5):
        response = request('GET', link)
        soup = BeautifulSoup(response.content)
        htmltext = soup.find_all(text=True)
        visibletext = filter(self.tag_visible, htmltext)
        cleantexts = [text for text in visibletext if len(text.split(' ')) > sensitivity]
        mergedtext = ' '.join(cleantexts)
        return mergedtext

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

class MemberManagement:
    def __init__(self):
        self.database = 'serverdata'

    def add_service(self, member_id, service, params):
        with datalink(self.database,service) as dl:
            dl.update_one({'member':member_id}, params, upsert=True)

    def get_service(self, member_id, service):
        with datalink(self.database, service) as dl:
            return dl.find_one({'member':member_id})

    def service_database(self, service):
        with datalink(self.database, service) as dl:
            return list(dl.find({}))


# Python Program for
# demonstrating the
# PyMongo Cursor to JSON

def export_rssentries():
    # Importing required modules
    from pymongo import MongoClient
    from bson.json_util import dumps, loads

    # Connecting to MongoDB server
    # client = MongoClient('host_name',
    # 'port_number')
    info = json.load(open("MONGODB"))
    client = MongoClient(info['hostname'], info['port'])

    # Connecting to the database named
    # GFG
    mydatabase = client.rssdata

    # Accessing the collection named
    # gfg_collection
    mycollection = mydatabase.rssentries

    # Now creating a Cursor instance
    # using find() function
    cursor = mycollection.find()

    # Converting cursor to the list
    # of dictionaries
    list_cur = list(cursor)

    # Converting to the JSON
    json_data = dumps(list_cur, indent=2)

    # Writing data to file data.json
    with open('dailywiredata.json', 'w') as file:
        file.write(json_data)

#export_rssentries()