
__author__ = 'xuke'

import traceback, threading, select
from random import choice
from string import maketrans

def ordlong(string):
  decimal = 0
  for i in range(len(string)):
    decimal += ord(string[i])*(256**(len(string)-i-1))
  return decimal

def chrlong(integer, length=2):
  string = ''
  for i in range(length):
    string += chr(integer/(256**(length-i-1))%256)
  return string

def generate_key(length=32):
  return ''.join((choice('abcdefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length)))


connection_id = 0
def generate_connection_id():
    global connection_id
    cid = connection_id
    connection_id += 1
    return cid

def db():
  traceback.print_exc()

def start_thread(target, daemon=True, args=None):
  if not args:
    th = threading.Thread(target=target)
  else:
    th = threading.Thread(target=target, args=args)
  th.setDaemon(daemon)
  th.start()

intab = ''
outtab = ''
for c in range(256):
    intab += chr(c)
    outtab += chr(c^200)
trantab = maketrans(intab, outtab)

def xor(src):
    return src.translate(trantab)

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)

    return reduce(lambda x,y:x+y, lst) if lst else ''

def pipe(reader_sock, writer_file):
    reader_sock.setblocking(0)
    while True:
        try:
            select.select([reader_sock], [], [])
            try:
                data = reader_sock.recv(1024)
                if data:
                    try:
                        writer_file.write(xor(data))
                    except KeyboardInterrupt:
                        raise
                    except: # writer socket closed
                        # shutdown_connection(reader_sock)
                        break
                else: # read end, socket closed
                    break
            except KeyboardInterrupt:
                raise
            except: # reader socket closed
                break
        except KeyboardInterrupt:
            raise
        except:
            break
    writer_file.loseConnection()

def shutdown_connection(connection):
    if type(connection) is list:
        for c in connection:
            shutdown_connection(c)
    else:
        try:
            connection.close()
        except:
            print "shutdown failed"
            pass
