#!/usr/bin/python

from toolkit import *
# from twisted.internet import protocol, reactor
import socket
from easynet import *

class ProxyProtocol(object):
    client_data = ""
    target = None
    remote_sock = None
    transport = None
    def dataReceived(self, data):
        if self.target:
            self.remote_sock.sendall(xor(data))
        else:
            self.client_data += data
            index = 0
            if len(self.client_data) < index+2:
                return
            target_len = ordlong(self.client_data[index:index+2])    
            index += 2
            if len(self.client_data) < index + target_len + 2:
                return
            target_host = xor(self.client_data[index:index+target_len])
            index += target_len
            target_port = ordlong(self.client_data[index:index+2])
            self.target = (target_host, target_port)
            index += 2
            
            try:
                self.remote_sock = socket.socket()
                self.remote_sock.connect(self.target)
                if len(self.client_data) > index:
                    self.remote_sock.sendall(xor(self.client_data[index:]))
            except:
                self.transport.loseConnection()
            else:
                response_pipe_thread = threading.Thread(target=pipe, args=(self.remote_sock, self.transport))
                response_pipe_thread.daemon = True
                response_pipe_thread.start()

    def loseConnection(self):
        try:
            self.remote_sock.close()
        except:
            pass

class ProxyFactory(object):
    def buildProtocol(self, addr):
        return ProxyProtocol()

reactor = Reactor()
reactor.listenTCP(3031, ProxyFactory())
try:
    reactor.run()
except KeyboardInterrupt:
    pass
