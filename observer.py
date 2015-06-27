# -*- coding: utf-8 -*-

class IObServer(object):

	def __init__(self):
		pass


	def update(self, id, name, value):
		print "update %s, %s, %s"%(id, name, value)

