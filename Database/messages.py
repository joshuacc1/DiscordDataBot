from Database.manage_mongo import ManageClient
import json

with open('SERVERPARAMS') as f:
    server_params = json.load(f)
    database_info = server_params['databases']['messages']
    DATABASE = database_info['database']
    COLLECTION = database_info['collection']

def addmessage(message_id, author, message, guild, channel, message_ref):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        db.insert_one({'message_id': message_id,
                       'author': str(author),
                       'message': message,
                       'guild': str(guild),
                       'channel': str(channel),
                       **message_ref})

def getmessage(in_message: str = ''):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        if in_message:
            return list(db.find({'message':{'$regex': ''.join(["*.",in_message,".*"])}}))
        else:
            return list(db.find({}))