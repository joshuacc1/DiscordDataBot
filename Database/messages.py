from manage_mongo import ManageClient

DATABASE = 'test_server_data'
COLLECTION = 'messages'
 

def addmessage(message_id, author, message, guild, channel, reply_message):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        db.insert_one({'message_id': message_id,
                       'author': str(author),
                       'message': message,
                       'guild': str(guild),
                       'channel': str(channel),
                       'reply_message': reply_message})

def getmessage(in_message: str = ''):
    with ManageClient() as client:
        db = client[DATABASE][COLLECTION]
        if in_message:
            return list(db.find({'message':{'$regex': ''.join(["*.",in_message,".*"])}}))
        else:
            return list(db.find({}))
        
addmessage('1234','author','message','guild','channel','reference')