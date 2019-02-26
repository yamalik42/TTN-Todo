import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["todoDB"]
col = db['todos']

query = {'_id': {'$in': [2,3]}}
x = col.delete_many(query)

all_records = list()
for record in col.find():
    print(record)


