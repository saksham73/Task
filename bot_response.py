import pymongo
import random

client= pymongo.MongoClient("mongodb+srv://saksham:saksham@cluster0-nvuma.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('db')


def botResponse(input, uname):
    res = db.chats.find_one({"user":input})
    if(db.chat_history.find_one( {"username":uname}) == None):
        db.chat_history.insert_one( {"username":uname,"bot":["Hey,"+uname+"!"],"user":[input] } )
    else:
        db.chat_history.update_one( {"username":uname}, {"$push":{"user":input}} )
    if(res == None):
        reply = "Out of context!"
        db.chat_history.update_one( {"username":uname}, {"$push":{"bot":reply}} )
        return reply
    #indx=random.randrange(0, len(res["response"]))
    db.chat_history.update_one( {"username":uname}, {"$push":{"bot":res["response"]}} )   
    return res["response"] 

def chat_history(username):
    chat = db.chat_history.find_one( {"username":username} )
    if(chat == None):
        return ""
    return chat 