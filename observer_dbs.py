# -*- coding: utf-8 -*-
import observer

class CObserver_Dbs(observer.IObServer):

	def __init__(self):
		super(CObserver_Dbs, self).__init__()

	def save(self, document):
		print "save %s"%(document,)
		document.queryset.save(document)


class CObserver_Dbs_Normal(CObserver_Dbs):

	pass


class CObserver_Dbs_RealTime(CObserver_Dbs):

	def __init__(self):
		super(CObserver_Dbs_RealTime, self).__init__()

	def update(self, id, name, value):
		print "update %s, %s, %s"%(id, name, value)

