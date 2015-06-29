# -*- coding: utf-8 -*-
import observer

class CObserver_Gas(observer.IObServer):

	def __init__(self):
		super(CObserver_Gas, self).__init__()
		self._dbsRpc = None

	def save(self, document):
		self._dbsRpc.savefromgas(document)


class CObserver_Gas_Normal(CObserver_Gas):

	pass


class CObserver_Gas_RealTime(CObserver_Gas):

	def __init__(self):
		super(CObserver_Gas_RealTime, self).__init__()

	def update(self, id, name, value):
		print "update %s, %s, %s"%(id, name, value)
		self._dbsRpc.updatefromgas(id, name, value)

