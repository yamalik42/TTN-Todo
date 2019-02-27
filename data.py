import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["todoDB"]
col = db['todos']
col.update_many({}, {"$set": {"Archived": False}})
all_records = list()
for record in col.find():
    print(record)


