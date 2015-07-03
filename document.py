# -*- coding: utf-8 -*-
import metaclasses
import observer

class Document(object):

	__metaclass__ = metaclasses.GetMetaClass()
	#observer = observer.IObServer()

	#扩展属性
	#dbname = "test"
	#collectionname = ""    #集合名
	#REAL_TIME_SAVE = False #即时存盘

	def __init__(self):
		pass

	def getid(self):
		return self._id



	#====for dbs======
	@classmethod
	def getcollection(cls):
		return cls.queryset.collection()

	#====for dbs======


	def save(self):
		self.__class__.observer.save(self)

	def childsetattr(self, namelist, value):
		self.__class__.observer.updatechild(self._id, namelist, value)


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
		for fields_name, fields in self.__class__._fields.iteritems():
			data[fields_name] = fields.to_python(self.__dict__.get(fields_name))
		data["_id"] = self._id
		return data


	def __setstate__(self, data):
		'''
		反序列化
		'''

		if not data.has_key("_id"):
			raise Exception("%s find not _id fields"%(self.__class__, )) #先简单要求必须有_id字段
		self.__dict__["_id"] = data.pop("_id")
		for fields_name, value in data.iteritems():
			fileds = self.__class__._fields.get(fields_name)
			if fileds is None:
				raise Exception("%s find not filed:%s"%(self.__class__, fields_name))
			self.__dict__[fields_name] = fileds.from_python(value)

		self.buildparent()



	def from_mongo(self, data):
		'''
		反序列化 存盘
		'''
		if not data.has_key("_id"):
			raise Exception("%s find not _id fields"%(self.__class__, )) #先简单要求必须有_id字段
		self.__dict__["_id"] = data.pop("_id")
		for fields_name, value in data.iteritems():
			fields = self.__class__._fields.get(fields_name)
			if fields is None:
				raise Exception("%s find not filed:%s"%(self.__class__, fields_name))
			self.__dict__[fields_name] = fields.from_mongo(value)

		self.buildparent()


	def to_mongo(self, needid=True):
		'''
		序列化 存盘的
		'''
		data = {}
		for fields_name, fields in self.__class__._fields.iteritems():
			data[fields_name] = fields.to_mongo(self.__dict__.get(fields_name))
		if needid:
			data["_id"] = self._id
		return data

	def create_default(self):
		for fields_name, fields in self.__class__._fields.iteritems():
			self.__dict__[fields_name] = fields.create_default()


	def buildparent(self):
		for fields_name, fields in self.__class__._fields.iteritems():
			fields.buildparent(self.__dict__.get(fields_name), self)
