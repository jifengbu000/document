# -*- coding: utf-8 -*-
import bson

class CQuerySet(object):

	def __init__(self, doc_cls, collection):
		self._doc_cls = doc_cls           #文档cls
		self._collection = collection     #pymongo collection对象


	def collection(self):
		return self._collection

	def create(self):
		doc = self._doc_cls()
		doc.create_default()
		object_id = self._collection.insert(doc.to_mongo(False))
		#!!!异常处理
		doc.__dict__["_id"] = object_id
		doc.buildparent()
		return doc


	def load(self, id):
		if type(id) != bson.ObjectId:
			id = bson.ObjectId(id)
		result = self._collection.find_one(id)
		if result is None:
			return None
		obj = self._doc_cls.__new__(self._doc_cls)
		obj.from_mongo(result)
		return obj


	def save(self, doc):
		#!!!异常处理
		self._collection.save(doc.to_mongo())

	def find(self, *args, **kwargs):
		d = {}
		for result in self._collection.find(*args, **kwargs):
			obj = self._doc_cls.__new__(self._doc_cls)
			obj.from_mongo(result)
			d[obj._id] = obj
		return d



