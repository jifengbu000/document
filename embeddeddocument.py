# -*- coding: utf-8 -*-
import metaclasses
import fields

class EmbeddedDocumentMetaClass(type):

	""" Metaclass for all EmbeddedDocument.
	"""

	def __new__(cls, name, bases, attrs):
		super_new = super(EmbeddedDocumentMetaClass, cls).__new__

		FORBIDEN_FIELD_NAMES = ["_fields", "_id", "_parent", "_myfields"]

		doc_fields = {}
		for attr_name, attr_value in attrs.items():
			if not isinstance(attr_value, fields.BaseField):
				continue
			if attr_name in FORBIDEN_FIELD_NAMES:
				raise Exception("%s cannot be a field name"%attr_name)
			doc_fields[attr_name] = attr_value
			attr_value.name = attr_name
			del attrs[attr_name]

		attrs['_fields'] = doc_fields

		doc_cls = super_new(cls, name, bases, attrs)

		return doc_cls



class EmbeddedDocument(object):

	__metaclass__ = EmbeddedDocumentMetaClass

	def __init__(self, fields):
		self._myfields = fields

	def childsetattr(self, namelst, value):
		namelst.append(self._myfields.name)
		self._parent.childsetattr(namelst, value)



	def __setattr__(self, name, value):
		filed = self.__class__._fields.get(name)
		if filed is None:
			return object.__setattr__(self, name, value)
		filed.validate(value)
		self._parent.childsetattr([name, self._myfields.name], value)
		return object.__setattr__(self, name, value)



	def __getstate__(self):
		'''
		序列化
		'''
		return self.to_python()


	def __setstate__(self, data):
		'''
		反序列化
		'''
		self.from_python(data)


	def to_python(self):
		data = {}
		for field_name, field in self.__class__._fields.iteritems():
			data[field_name] = field.to_python(self.__dict__.get(field_name))
		return data


	def from_python(self, data):
		for field_name, value in data.iteritems():
			filed = self.__class__._fields.get(field_name)
			if filed is None:
				raise Exception("%s find not filed:%s"%(self.__class__, field_name))
			self.__dict__[field_name] = filed.from_python(value)



	def from_mongo(self, data):
		'''
		反序列化 存盘
		'''
		for field_name, value in data.iteritems():
			filed = self.__class__._fields.get(field_name)
			if filed is None:
				raise Exception("%s find not filed:%s"%(self.__class__, field_name))
			self.__dict__[field_name] = filed.from_mongo(value)


	def to_mongo(self):
		'''
		序列化 存盘的
		'''
		data = {}
		for field_name, field in self.__class__._fields.iteritems():
			data[field_name] = field.to_mongo(self.__dict__.get(field_name))
		return data

	def create_default(self):
		for fields_name, fields in self.__class__._fields.iteritems():
			self.__dict__[fields_name] = fields.create_default()


	def buildparent(self):
		data = {}
		for fields_name, fields in self.__class__._fields.iteritems():
			data[fields_name] = fields.buildparent(self.__dict__.get(fields_name), self)
		return data

