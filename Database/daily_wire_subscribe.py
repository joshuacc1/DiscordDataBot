from Database.manage_mongo import ManageClient
import feedparser
import json
from pprint import pprint

with open('SERVERPARAMS') as f:
    server_params = json.load(f)
    database_info = server_params['databases']['subscribers']
    DATABASE = database_info['database']
    COLLECTION = database_info['collection']

# DATABASE = 'test_server_data'
# COLLECTION = 'test_subscribers'

def add_keyword(member_id, keyword):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        status = db.update_one({'member':member_id},
                                {'$addToSet': {'keywords': keyword}},
                                upsert = True)
        return status

def remove_keyword(member_id, keyword):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        status = db.update_one({'member':member_id},
                                {'$pull': {'keywords': keyword}},
                                upsert = True)
        return status

def add_author(member_id, author):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        status = db.update_one({'member':member_id},
                                {'$addToSet': {'authors': author}},
                                upsert = True)
        return status

def remove_author(member_id, author):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        status = db.update_one({'member':member_id},
                                {'$pull': {'authors': author}},
                                upsert = True)
        return status
    
def get_keywords(member_id):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        result = db.find_one({'member':member_id})
        if result is None:
            return []
        if 'keywords' in result:
            return result['keywords']
        else:
            return []

def get_author(member_id):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        result = db.find_one({'member':member_id})
        if result is None:
            return []
        if 'authors' in result:
            return result['authors']
        else:
            return []
        
def get_subscribers_with_match(text):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        result = db.find()
        members = []
        for res in result:
            if any([keyword in text for keyword in  res['keywords']]):
                members.append(res['member'])
        return members

def get_subscribers_with_author(input_author):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        result = db.find()
        members = []
        for res in result:
            if any([author in input_author for author in  res['authors']]):
                members.append(res['member'])
        return members
    
