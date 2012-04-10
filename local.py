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
                                    self.server_sock.sendall(xor(data))
                                else:
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
    servsock = socket.socket()
    servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servsock.bind(config.local_bind_addr)
    servsock.listen(1000)

    print "--> " + "%s:%s" % config.local_bind_addr + " --> " + "%s:%s" % config.server_proxy_addr + " -->"

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
        # socks_ret = socks.accept(client_sock)
        server_sock = socket.socket()
        server_sock.connect(config.server_proxy_addr)
        proxy = ProxyThread()
        proxy.daemon = True
        proxy.set_socks(client_sock, server_sock)
        proxy.start()
except KeyboardInterrupt:
    print
