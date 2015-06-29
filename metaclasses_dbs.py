# -*- coding: utf-8 -*-
import fields
from queryset import CQuerySet
import connection
import observer_dbs

DEFAULT_DB = "test"

connection.register_connection(DEFAULT_DB,name=DEFAULT_DB,
							   host="localhost",port=None,
							   username=None, password=None)

class DbsDocumentMetaclass(type):

	""" Metaclass for all dbs documents.
	"""

	def __new__(cls, name, bases, attrs):
		super_new = super(DbsDocumentMetaclass, cls).__new__

		FORBIDEN_FIELD_NAMES = ["_fields", "_id", "queryset", "dbname", "collectionname", "observer"]

		doc_fields = {}
		for attr_name, attr_value in attrs.items():
			if not isinstance(attr_value, fields.BaseField):
				continue
			if attr_name in FORBIDEN_FIELD_NAMES:
				raise Exception("%s cannot be a field name"%attr_name)
			doc_fields[attr_name] = attr_value
			del attrs[attr_name]
			
		attrs['_fields'] = doc_fields

		real_time_save = attrs.pop("real_time_save", False)
		if real_time_save:
			attrs["observer"] = observer_dbs.CObserver_Dbs_Normal()
		else:
			attrs["observer"] = observer_dbs.CObserver_Dbs_RealTime()

		querysetcls = getattr(attrs, "queryset", CQuerySet)
		db = connection.get_db(getattr(attrs, "dbname", DEFAULT_DB))
		collection = db[getattr(attrs, "collectionname", name)]

		doc_cls = super_new(cls, name, bases, attrs)

		doc_cls.queryset = querysetcls(doc_cls, collection)

		return doc_cls

