# -*- coding: utf-8 -*-
import rpyc

import test


#创建SocketServerTCP服务器：
import SocketServer
from SocketServer import StreamRequestHandler as SRH
from time import ctime,sleep
import struct
import cPickle


host = 'localhost'
port = 18861
addr = (host,port)

class Servers(SRH):
	def handle(self):
		print 'got connection from ',self.client_address
		#self.wfile.write('connection %s:%s at %s succeed!' % (host,port,ctime()))
		datastr = ""
		while True:
			data = self.request.recv(1024)
			if not data:
				break
			print "RECV from ", self.client_address[0]
			datastr += data
			if len(datastr) < 4:
				continue
			msglen = struct.unpack("i", datastr[:4])[0]
			if len(datastr) >= msglen + 4:
				msgstr = datastr[4:msglen+4]
				datastr = datastr[msglen+4:]
				self.handlemsg(msgstr)
			sleep(0.05)

	def handlemsg(self, msgstr):
		msg = cPickle.loads(msgstr)
		rtmsg =msg.handle()
		rtmsgstr = cPickle.dumps(rtmsg)
		self.request.send(rtmsgstr)



print 'server is running....'
server = SocketServer.ThreadingTCPServer(addr,Servers)
server.serve_forever()



