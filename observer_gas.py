# -*- coding: utf-8 -*-
import observer

class CObserver_Gas(observer.IObServer):

	def __init__(self, doccls):
		super(CObserver_Gas, self).__init__(doccls)
		self._dbsRpc = None

	def save(self, document):
		self._dbsRpc.save(document)

	def updatechild(self, id, namelist, value):
		print "updatechild %s, %s, %s"%(id, namelist, value)


class CObserver_Gas_Normal(CObserver_Gas):

	pass


class CObserver_Gas_RealTime(CObserver_Gas):

	def update(self, id, name, value):
		print "update %s, %s, %s"%(id, name, value)
		self._dbsRpc.update(id, name, value)


	def updatechild(self, id, namelist, value):
		print "updatechild %s, %s, %s"%(id, namelist, value)
		self._dbsRpc.updatechild(id, namelist, value)

