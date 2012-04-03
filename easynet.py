
import socket, select
class AutoFlushWriter(object):
    def __init__(self, writer):
        self.writer = writer
    def write(self, data):
        self.writer.write(data)
        self.writer.flush()
        
    def loseConnection(self):
        try:
            self.writer.close()
        except:
            pass

class Reactor(object):
    servsock = None
    socklist = []
    factory = None
    connection_handlers = {}
    def listenTCP(self, addr, factory):
        self.servsock = socket.socket()
        self.servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsock.bind(("0.0.0.0", addr) if type(addr) is int else addr)
        self.servsock.listen(10)
        self.socklist.append(self.servsock)
        self.factory = factory
    
    def run(self):
        while True:
            while True:
                try:
                    socks = None
                    socks, _, _ = select.select(self.socklist, [], [], 3)
                except KeyboardInterrupt:
                    print "Killed"
                    raise
                except:
                    print "error"
                    return
                else:
                    if socks:
                        break
            for sock in socks:
                if sock is self.servsock:
                    reqcon, addr = self.servsock.accept()
                    handler = self.factory.buildProtocol(addr)
                    handler.transport = AutoFlushWriter(reqcon.makefile("wb"))
                    self.connection_handlers[reqcon] = handler
                    self.socklist.append(reqcon)
                    reqcon.setblocking(False)
                else:
                    handler = self.connection_handlers[sock]
                    try:
                        data = sock.recv(1024)
                    except KeyboardInterrupt:
                        raise
                    except:
                        self.socklist.remove(sock)
                        del self.connection_handlers[sock]
                    else:
                        if data:
                            try:
                                handler.dataReceived(data)
                            except:
                                # handler.connectionLost()
                                handler.transport.loseConnection()
                        else:
                            self.socklist.remove(sock)
                            del self.connection_handlers[sock]
