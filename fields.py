# -*- coding: utf-8 -*-
from errors import *

__all__ = [
	"IntField", "LongField", "FloatField","BooleanField",
    "StringField",
]

class BaseField(object):
	name = None
	DEFAULT_VALUE = None
	def __init__(self, default=None):
		if default is None:
			self.default = self.DEFAULT_VALUE
		else:
			self.default = default
	
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


#class EmbeddedDocumentField(BaseField)


