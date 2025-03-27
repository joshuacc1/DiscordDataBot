from pymongo import MongoClient, DESCENDING
import json

def database_info():
    mongo_server_info = {'port': 27017, 'host': 'localhost'}
    client = MongoClient(mongo_server_info['host'], mongo_server_info['port'])
    db_list = client.list_database_names()
    for db in db_list:
        print(db)
        for coll in client[db].list_collection_names():
            print("-->",coll)
            print(client[db][coll].count_documents({}), " total documents")

class ManageClient:
    def __init__(self):
        self.info = json.load(open("MONGODB"))
        
    def __enter__(self):
        self.client = MongoClient(self.info['hostname'],self.info['port'])
        return self.client

    def __exit__(self, type, value, traceback):
        if self.client:
            self.client.close()

def get_client():
    info = json.load(open('MONGODB','r'))
    client = MongoClient(info['hostname'], info['port'])
    return client

def get_collection(database_name, collection_name):
    info = get_client()
    client = MongoClient(info['hostname'], info['port'])
    coll = client[database_name][collection_name]
    return coll

def remove_collection(database_name, collection_name):
    with MongoClient() as client:
        if collection_name in client[database_name].list_collection_names():
            client[database_name].drop_collection(collection_name)

def remove_database(database_name):
    with MongoClient() as client:
        if database_name in client.list_database_names():
            client.drop_database(database_name)

if __name__=="__main__":
    # get_client()
    database_info()
    # print("\nadding collection\n")
    # coll = get_collection('server_data','links')
    # coll.insert_one({'name':'test'})
    # database_info()
    # print("\nremoving collection\n")
    # remove_collection('server_data','links')
    # database_info()
    # remove_database('server_data')
    #remove_database('test_server_data')
    # database_info()
    # print("done")