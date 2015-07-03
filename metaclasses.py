# -*- coding: utf-8 -*-
import game


def GetDbsDocumentMetaclass():
	import metaclasses_dbs
	return metaclasses_dbs.DbsDocumentMetaclass

def GetGasDocmentMetaclass():
	import metaclasses_gas
	return metaclasses_gas.GasDocumentMetaclass

def GetMetaClass():
	if game.IsDbs():
		return GetDbsDocumentMetaclass()
	elif game.IsGas():
		return GetGasDocmentMetaclass()
	else:
		return type
