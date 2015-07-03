# -*- coding: utf-8 -*-
import fields
import observer_gas

class GasDocumentMetaclass(type):

	""" Metaclass for all gas documents.
	"""

	def __new__(cls, name, bases, attrs):
		super_new = super(GasDocumentMetaclass, cls).__new__

		FORBIDEN_FIELD_NAMES = ["_fields", "_id", "REAL_TIME_SAVE", "observer"]

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

		real_time_save = attrs.pop("REAL_TIME_SAVE", False)
		if real_time_save:
			doc_cls.observer = observer_gas.CObserver_Gas_RealTime(doc_cls)
		else:
			doc_cls.observer = observer_gas.CObserver_Gas_Normal(doc_cls)


		return doc_cls

