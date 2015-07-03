# -*- coding: utf-8 -*-

class IObServer(object):

	def __init__(self, doccls):
		self._doccls = doccls


	def update(self, id, name, value):
		print "update %s, %s, %s"%(id, name, value)

	def updatechild(self, id, namelst, value):
		print "updatechild %s, %s, %s"%(id, namelst, value)

	def save(self, document):
		pass

