# -*- coding: utf-8 -*-
import game


def GetDbsDocumentMetaclass():
	import metaclasses_dbs
	return metaclasses_dbs.DbsDocumentMetaclass

def GetGasDocmentMetaclass():
	import metaclasses_gas
	return metaclasses_gas.GasDocumentMetaclass

def GetMetaClass():
	if game.isdbs():
		return GetDbsDocumentMetaclass()
	elif game.isgas():
		return GetGasDocmentMetaclass()
	else:
		return type
