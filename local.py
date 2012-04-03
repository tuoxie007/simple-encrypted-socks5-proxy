#!/usr/bin/python

from toolkit import *
from twisted.internet import protocol, reactor
from socket import socket

SOCKS_VER5 = "\x05"
METHOD_NO_AUTHENTICATION_REQUIRED = '\x00'
METHOD_GSSAPI = '\x01'
METHOD_USERNAME_PASSWORD = '\x02'
METHOD_IANA_ASSIGNED_MIN = '\x03'
METHOD_IANA_ASSIGNED_MAX = '\x7F'
METHOD_RESERVED_FOR_PRIVATE_METHODS_MIN = '\x80'
METHOD_RESERVED_FOR_PRIVATE_METHODS_MAX = '\xFE'
METHOD_NO_ACCEPTABLE_METHODS = '\xFF'

CMD_CONNECT = '\x01'
CMD_BIND = '\x02'
CMD_UDP = '\x03'

RSV = '\x00'
ATYP_IPV4 = '\x01'
ATYP_DOMAINNAME = '\x03'
ATYP_IPV6 = '\x04'

REP_succeeded = '\x00'
REP_general_SOCKS_server_failure = '\x01'
REP_connection_not_allowed_by_ruleset = '\x02'
REP_Network_unreachable = '\x03'
REP_Host_unreachable = '\x04'
REP_Connection_refused = '\x05'
REP_TTL_expired = '\x06'
REP_Command_not_supported = '\x07'
REP_Address_type_not_supported = '\x08'

class ProxyProtocal(protocol.Protocol):
    replied_socks = False
    socks_data = ""
    target = None
    remote_sock = None
    def dataReceived(self, data):
        print "received from client %s" % len(data)
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
                self.remote_sock = socket()
                self.remote_sock.connect(("127.0.0.1", 3031))
                self.remote_sock.sendall(chrlong(len(self.target[0])) + xor(self.target[0]) + chrlong(self.target[1]))
            except:
                self.transport.write(SOCKS_VER5 + REP_Network_unreachable)
            else:
                self.transport.write(SOCKS_VER5 + REP_succeeded + RSV + address_type + domain_length + domain + port)
                response_pipe_thread = threading.Thread(target=pipe, args=(self.remote_sock, self.transport))
                response_pipe_thread.start()

class ProxyFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ProxyProtocal()


reactor.listenTCP(3030, ProxyFactory())
try:
    reactor.run()
except KeyboardInterrupt:
    pass
