#!/usr/bin/python

from toolkit import *
# from twisted.internet import protocol, reactor
import socket, sys
from socks import *
from easynet import *

class ProxyProtocol(object):
    replied_socks = False
    socks_data = ""
    target = None
    remote_sock = None
    transport = None
    def dataReceived(self, data):
        if self.target:
            self.remote_sock.sendall(xor(data))
        else:
            if not self.replied_socks:
                self.transport.write(SOCKS_VER5)
                self.transport.write(METHOD_NO_AUTHENTICATION_REQUIRED)
                self.replied_socks = True
            
            self.socks_data += data
            index = 0
            if len(self.socks_data) < index+2:
                return
            socks_version = self.socks_data[index]
            index += 1
            method_number = ord(self.socks_data[index])
            index += 1
            if len(self.socks_data) < index+method_number+4:
                return
            methods_client_supported = self.socks_data[index:index+method_number]
            index += method_number
            
            socks_version = self.socks_data[index]
            index += 1
            command = self.socks_data[index]
            index += 1
            rsv = self.socks_data[index]
            index += 1
            address_type = self.socks_data[index]
            index += 1
            if address_type == ATYP_DOMAINNAME:
                if len(self.socks_data) < index+1:
                    return
                domain_length = self.socks_data[index]
                index += 1
                if len(self.socks_data) < index+ord(domain_length)+2:
                    return
                domain = self.socks_data[index:index+ord(domain_length)]
                hostname = domain
                index += ord(domain_length)
                port = self.socks_data[index:index+2]
                index += 2
            elif address_type == ATYP_IPV4:
                domain_length = ''
                if len(self.socks_data) < index+6:
                    return
                domain = self.socks_data[index:index+4]
                hostname = '%s.%s.%s.%s' % (str(ord(domain[0])), str(ord(domain[1])), str(ord(domain[2])), str(ord(domain[3])))
                index += 4
                port = self.socks_data[index:index+2]
                index += 2
             #read command over
            
            self.target = (hostname, ordlong(port))
            try:
                self.remote_sock = socket.socket()
                global proxy_host, proxy_port
                self.remote_sock.connect((proxy_host, proxy_port))
                self.remote_sock.sendall(chrlong(len(self.target[0])) + xor(self.target[0]) + chrlong(self.target[1]))
            except:
                self.transport.write(SOCKS_VER5 + REP_Network_unreachable)
            else:
                self.transport.write(SOCKS_VER5 + REP_succeeded + RSV + address_type + domain_length + domain + port)
                response_pipe_thread = threading.Thread(target=pipe, args=(self.remote_sock, self.transport))
                response_pipe_thread.daemon = True
                response_pipe_thread.start()

class ProxyFactory(object):
    def buildProtocol(self, addr):
        return ProxyProtocol()

proxy_host = "your_proxy_server_hostname"
proxy_port = 3031
reactor = Reactor()
reactor.listenTCP(3030, ProxyFactory())
try:
    reactor.run()
except KeyboardInterrupt:
    pass
