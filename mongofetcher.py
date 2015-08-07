from pymongo import MongoClient

class MongoFetcher():
	def __init__(self,db):
		self.db = db
		self.dbClient = MongoClient('localhost', 27017)[db]
	def getItems(self,coll, **kwargs):
		dbClient = self.dbClient
		items = dbClient[coll].find(kwargs)
		return list(items[:])