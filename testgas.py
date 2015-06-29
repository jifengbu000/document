# -*- coding: utf-8 -*-

import rpyc
import game
game.__dict__["bdbs"] = False
game.__dict__["bgas"] = True


import test


from socket import *

host = 'localhost'
port = 18861
bufsize = 1024
addr = (host,port)




def sendmsg(client, msg):
	import cPickle
	import struct
	msgstr = cPickle.dumps(msg)
	client.send("%s%s"%(struct.pack('i',len(msgstr)),msgstr))
	data = client.recv(bufsize)
	print data, len(data)
	retmsg = cPickle.loads(data)
	return retmsg


client = socket(AF_INET,SOCK_STREAM)
client.connect(addr)

playerrpc = test.CRpc(sendmsg, client)
test.CPlayer.observer._dbsRpc = playerrpc

loadmsg = test.CLoadPlayers()
players = sendmsg(client, loadmsg)

print players

for k,v in players.iteritems():
	print k,v
	v.charName = "efwfe"
	#v.save()

client.close()