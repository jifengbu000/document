# -*- coding: utf-8 -*-

import fields



import sys


from document import Document
from fields import *


class CPlayer(Document):
	charName = StringField()

	real_time_save = True

'''
player = CPlayer.queryset.create()

print player.__dict__
'''
"""

obj = CPlayer.queryset.load("558e6c8bbe5f7b0d180625bb")

print obj
print obj.__dict__

obj.charName = "33"
obj.save()

for each in CPlayer.getcollection().find({}):
	print each
	"""

class CRpcMsg(object):

	def __init__(self):
		self

	def handle(self):
		pass

class CLoadPlayers(object):

	def handle(self):
		return CPlayer.queryset.find()


class CRpcMsg(object):
	def __init__(self, fc, args):
		self.fc = fc
		self.args = args

	def handle(self):
		func = getattr(CPlayer, self.fc)
		return func(*self.args)

class CRpc(object):

	def __init__(self, sendmsgfunc, client):
		self.fc = ""
		self.args = None
		self.sendmsgfunc = sendmsgfunc
		self.client =client

	def __getattr__(self, name):
		self.fc =name
		return self.SendMc

	def SendMc(self,*args):
		self.args=args
		self.sendmsgfunc(self.client, CRpcMsg(self.fc,self.args))


