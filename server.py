#!/usr/bin/python

import socket, sys, select, threading, socks, config
from toolkit import *

class ProxyThread(threading.Thread):
    def set_socks(self, client_sock, server_sock):
        self.server_sock = server_sock
        self.client_sock = client_sock
    def run(self):
        while True:
            end = False
            try:
                socks = select.select([self.client_sock, self.server_sock], [], [], 3)[0]
            except:
                end = True
            else:
                for sock in socks:
                    try:
                        data = sock.recv(1024)
                    except:
                        end = True
                    else:
                        if not data:
                            end = True
                        else:
                            try:
                                if sock is self.client_sock:
                                    #print "%s bytes from client" % len(data)
                                    self.server_sock.sendall(xor(data))
                                else:
                                    #print "%s bytes from server" % len(data)
                                    self.client_sock.sendall(xor(data))
                            except:
                                end = True
            if end:
                try:
                    self.clien_sock.close()
                except:
                    pass
                try:
                    self.server_sock.close()
                except:
                    pass
                break
    

try:
    proxy_host = "tuoxie.me"
    proxy_port = 3031

    servsock = socket.socket()
    servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servsock.bind(config.server_bind_addr)
    servsock.listen(1000)

    print "--> " + "%s:%s" % config.server_bind_addr + " -->"

    while True:
        while True:
            try:
                sock = None
                sock = select.select([servsock], [], [], 3)[0]
            except KeyboardInterrupt:
                raise
            except:
                raise
            else:
                if sock:
                    break
        client_sock, client_addr = servsock.accept()
        socks_ret = socks.accept(client_sock, True)
        if not socks_ret:
            continue
        server_sock = socket.socket()
        server_sock.settimeout(3)
        try:
            server_sock.connect(socks_ret[0])
        except KeyboardInterrupt:
            raise
        except:
            #print "failed to connect to %s" % str(socks_ret[0])
            socks.reply(client_sock, socks_ret[1], True, False)
        else:
            server_sock.settimeout(None)
            port = server_sock.getsockname()[1]port = server_sock.getsockname()[1]
            bindaddr={'address_type': chr(0x01),
                      'domain_length': '',
                      'domain': socket.inet_aton(server_sock.getsockname()[0]),
                      'port': chr(port/256) + chr(port%256)}
            socks.reply(client_sock, bindaddr, True, True)
            proxy = ProxyThread()
            proxy.daemon = True
            proxy.set_socks(client_sock, server_sock)
            proxy.start()
except KeyboardInterrupt:
    print
