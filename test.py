# -*- coding: utf-8 -*-

import fields



import sys


from document import Document
from fields import *


class CPlayer(Document):
	charName = StringField()

'''
player = CPlayer.queryset.create()

print player.__dict__
'''


obj = CPlayer.queryset.load("558e6c8bbe5f7b0d180625bb")

print obj
print obj.__dict__

obj.charName = "222"
obj.save()

for each in CPlayer.getcollection().find({}):
	print each