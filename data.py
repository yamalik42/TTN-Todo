import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["todoDB"]
col = db['todos']

for data in col.find():
    print(data)

