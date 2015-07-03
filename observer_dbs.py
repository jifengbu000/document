# -*- coding: utf-8 -*-
import observer

class CObserver_Dbs(observer.IObServer):

	def save(self, document):
		self._doccls.queryset.save(document)


class CObserver_Dbs_Normal(CObserver_Dbs):

	pass


class CObserver_Dbs_RealTime(CObserver_Dbs):

	def update(self, id, name, value):
		fields = self._doccls._fields.get(name)
		if fields is None:
			return
		self._doccls.getcollection().update({"_id":id}, {name:fields.to_mongo(value)})

	def updatechild(self, id, namelst, value):
		namelst.reverse()
		fields = self._doccls
		for fields_name in namelst:
			if fields == self._doccls:
				fields = fields._fields.get(fields_name)
			else:
				fields = fields.document_type._fields.get(fields_name)
		name = ".".join(namelst)
		self._doccls.getcollection().update({"_id":id}, {"$set": {name:fields.to_mongo(value)}})


