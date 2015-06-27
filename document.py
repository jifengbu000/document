# -*- coding: utf-8 -*-
import metaclasses
import observer

class Document(object):

	__metaclass__ = metaclasses.GetMetaClass()
	observer = observer.IObServer()
	#queryset = None
	#dbname = "" #
	def __init__(self):
		pass

	def GetID(self):
		return self._id


	@classmethod
	def getcollection(cls):
		return cls.queryset.collection()

	def save(self):
		self.queryset.save(self)

	def __setattr__(self, name, value):
		filed = self.__class__._fields.get(name)
		if filed is None:
			return object.__setattr__(self, name, value)
		filed.validate(value)
		self.__class__.observer.update(self._id, name, value)
		return object.__setattr__(self, name, value)



	def __getstate__(self):
		'''
		序列化
		'''
		data = {}
		for field_name, field in self.__class__._fields.iteritems():
			data[field_name] = field.to_python(self.__dict__.get(field_name))
		data["_id"] = self._id
		return data


	def __setstate__(self, data):
		'''
		反序列化
		'''

		if not data.has_key("_id"):
			raise Exception("%s find not _id fields"%(self.__class__, )) #先简单要求必须有_id字段
		self.__dict__["_id"] = data.pop("_id")
		for field_name, value in data.iteritems():
			filed = self.__class__._fields.get(field_name)
			if filed is None:
				raise Exception("%s find not filed:%s"%(self.__class__, field_name))
			self.__dict__[field_name] = filed.from_python(value)


	def from_mongo(self, data):
		'''
		反序列化 存盘
		'''
		if not data.has_key("_id"):
			raise Exception("%s find not _id fields"%(self.__class__, )) #先简单要求必须有_id字段
		self.__dict__["_id"] = data.pop("_id")
		for field_name, value in data.iteritems():
			filed = self.__class__._fields.get(field_name)
			if filed is None:
				raise Exception("%s find not filed:%s"%(self.__class__, field_name))
			self.__dict__[field_name] = filed.from_mongo(value)


	def to_mongo(self, needid=True):
		'''
		序列化 存盘的
		'''
		data = {}
		for field_name, field in self.__class__._fields.iteritems():
			data[field_name] = field.to_mongo(self.__dict__.get(field_name))
		if needid:
			data["_id"] = self._id
		return data

