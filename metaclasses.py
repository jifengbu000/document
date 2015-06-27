# -*- coding: utf-8 -*-
import fields
from queryset import CQuerySet
import connection

class BaseDocumentMetaclass(type):

	""" Metaclass for all documents.
	"""

	def __new__(cls, name, bases, attrs):
		super_new = super(BaseDocumentMetaclass, cls).__new__


		doc_fields = {}
		for attr_name, attr_value in attrs.items():
			if not isinstance(attr_value, fields.BaseField):
				continue
			doc_fields[attr_name] = attr_value
			del attrs[attr_name]
			
		attrs['_fields'] = doc_fields
		
		return super_new(cls, name, bases, attrs)

DEFAULT_DB = "test"

connection.register_connection(DEFAULT_DB,name=DEFAULT_DB,host="localhost")

class DbsDocumentMetaclass(BaseDocumentMetaclass):

	def __new__(cls, name, bases, attrs):
		super_new = super(DbsDocumentMetaclass, cls).__new__

		doc_cls = super_new(cls, name, bases, attrs)

		querysetcls = getattr(attrs, "queryset", CQuerySet)
		db = connection.get_db(getattr(attrs, "dbname", DEFAULT_DB))
		collection = db[getattr(doc_cls, "collectionname", doc_cls.__name__)]
		doc_cls.queryset = querysetcls(doc_cls, collection)

		return doc_cls


def GetMetaClass():
	return DbsDocumentMetaclass