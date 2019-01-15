#!/usr/bin/env python

import pymongo

myclient = pymongo.MongoClient("mongodb://127.0.0.1/")
dblist = myclient.list_database_names()

mydb = myclient["gunpowder-printer"]
mycol = mydb["images"]

q = { "timesent" : 123 }
entry = { "timesent" : 123, "image64" : "python-test"}
mycol.insert_one(entry)

for i in mycol.find(q):
	print(i)
