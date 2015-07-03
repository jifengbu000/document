# -*- coding: utf-8 -*-
from errors import *


__all__ = [
	"BaseField", "IntField", "LongField", "FloatField","BooleanField",
    "StringField", "EmbeddedDocumentField",
]

class BaseField(object):
	name = None
	DEFAULT_VALUE = None
	def __init__(self, name=None,default=None):
		if default is None:
			self.default = self.DEFAULT_VALUE
		else:
			self.default = default
		self.name = name

	def validate(self, value):
		return True

	def error(self, message=""):
		"""Raises a ValidationError.
		"""
		raise ValidationError(message)

	def to_mongo(self, value):
		if value is None:
			return self.default
		return value

	def from_mongo(self, value):
		return value

	def to_python(self, value):
		return value

	def from_python(self, value):
		return value

	def create_default(self):
		return self.DEFAULT_VALUE

	def buildparent(self, value, parent):
		pass


class IntField(BaseField):
	DEFAULT_VALUE = 0

	def validate(self, value):
		if not isinstance(value, int):
			self.error('IntField only accepts int values, field:%s value:%s'%(self,value))
			return False
		return True


class LongField(BaseField):
	DEFAULT_VALUE = 0L

	def validate(self, value):
		if not isinstance(value, long):
			self.error('LongField only accepts long values, field:%s value:%s'%(self,value))
			return False
		return True


class FloatField(BaseField):
	DEFAULT_VALUE = 0.0

	def validate(self, value):
		if isinstance(value, int):
			value = float(value)
		if not isinstance(value, float):
			self.error('FloatField only accepts float values, field:%s value:%s'%(self,value))
			return False
		return True


class BooleanField(BaseField):
	DEFAULT_VALUE = False

	def validate(self, value):
		if not isinstance(value, bool):
			self.error('BooleanField only accepts boolean values, field:%s value:%s'%(self,value))
			return False
		return True


class StringField(BaseField):
	DEFAULT_VALUE = ""

	def validate(self, value):
		if not isinstance(value, str):
			self.error('StringField only accepts str values, field:%s value:%s'%(self,value))
			return False
		return True


class EmbeddedDocumentField(BaseField):

	def __init__(self, document_type, **kwargs):
		from embeddeddocument import EmbeddedDocument
		if not issubclass(document_type, EmbeddedDocument):
			self.error('Invalid embedded document class provided to an '
						'EmbeddedDocumentField')
		self.document_type = document_type
		super(EmbeddedDocumentField, self).__init__(**kwargs)

	def to_mongo(self, value):
		if value is None:
			value = self.document_type(self)
		return value.to_mongo()

	def from_mongo(self, value):
		obj = self.document_type(self)
		obj.from_mongo(value)
		return obj

	def to_python(self, value):
		return value.to_python()

	def from_python(self, value):
		obj = self.document_type(self)
		obj.from_python(value)
		return obj

	def validate(self, value):
		if not isinstance(value, self.document_type):
			self.error('Invalid embedded document instance provided to an '
					   'EmbeddedDocumentField')
			return False
		return self.document_type.validate(value)

	def buildparent(self, value, parent):
		value._parent = parent
		value.buildparent()

	def create_default(self):
		obj = self.document_type(self)
		obj.create_default()
		return obj


