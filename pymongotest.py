__author__ = 'xuxunpan'


import pymongo

client = pymongo.MongoClient(host="localhost")
db = client.testdb


for item in db.c_player.find():
	print item
