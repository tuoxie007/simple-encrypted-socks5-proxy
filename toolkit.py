
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

#print toHex('\x01\x12\n')
#print '38915c754c7a10c3840657f63e8d941407e716b45c41f777b43586f677b033362d7b365e6c56de74c941fe8190047eee865543c5c3d29ffc508a0ddce4611868d708219ce0fc50b1578a3bd202d062c4e67830bf53fd93626638efc8fbb9f2374f90aedbf2c11ac4254c3f2a41634fc8bca710e80a2ac1c16ad41a1ea02aa55a058ab26608ee0a031ac17269c002ae7a8019b138360bcf1ab993a4b5ac3f60f7a9afa08d753f1cc30bddc418a446fa838889af02cd9ccc6468240d2600817306083aebe481694fb3408c5ec825d61c4f58f873d8b52d18a4252a822eb6c3ac8917a957ebbf2bac9a283ee6962a098a3cc035ceed16a9c1780bfb881f410fc6646e60b20a72f83bea18f9c15059e1b24ec0c021f8806f80a3908f10ddb0e6e462dace7e6a294ca0b9458778af0631c10dd126b8db71a2ce388a1f5c47ae258a9f1c037b29f5e38716e998a59e0081792d40062f867e00aa44eda5c655abef6a832fee80faf82fd42115a92e96ca8e6f4be687904960fbc6488e46870f16ea04d4e73a29f16cd1e5c0371cf5eef7f4f2257cf3cb3a4ee641c852274ed8c17c87ec1ccea9a8d38c08a5d8c884f028120d9fce60c716f60c2279f68710c501806afc83deeb00859dea3cba54572d4d4192d0f3bea769e78f3e00c16ae84baf9872da2e10851178e56ac8917300adfb87250999461403cacaa9d8d0f1cdcc6a8b08a6259f3b033312bddae75298af206da891aa4ce553272a32ad20fc76ce6ba35092fc011c76bebb4417dfd8103697c9496966890876269f3b033312498dcfeb0b38dfce96aac8be404374dbe50ab856ed640bfc9204d4ee83600e5555d4239fc848e85ccef3a24d9b4e0ba1d8c94087d64c8cccec243f5f89303a367f49bba91e334359c01dbe8e257e120d7e0a4c8d89945766b63261150ef6149b2c83593c8864464b93a88d7ec346c01bc19d0d0c6dea1296dced41e4917370670cd6f06afa492af62d87a1f4065e968a550dd43563761ba6bf7242ee4a624fe48b8cd1ca6c26bc0970620634ea0c9821b92837ba72ba5e1cd109da258475d300c58edc1ea6745216510b3225bc9ca5ccfced30c75d00dae7d145d02986ced10972cc23da967f8978fa211ce63e603c05b37e9f5fbe2242194dee9fd5c40d75309ec7fb1da50283992cf6ed36425f9409843b21e57d61e68801143723adc658c40c4db0b8b80a16f7338ceb05a98a750791f89b1c5a57092a294ad03cce2ea173490d4f01fae484b8bfc3018ac6724fc7cda5feaabc74c38ae0df2e81f4817411c4ce68882397c9a0fc4d0a4429cf70f66acfd2acd8b19f1cc9e5928728107e1313691315dd159444a543238f9949ebe217cc5e0f939a7d1512c107b0cecee320fddbd01555c144e4699b10842900d7a5413219e660cb0ef328e179e34eb58354bed23ec145a0'[:1520]
#print '38915c754c7a10c3840657f63e8d941407e716b45c41f777b43586f677b033362d7b365e6c56de74c941fe8190047eee865543c5c3d29ffc508a0ddce4611868d708219ce0fc50b1578a3bd202d062c4e67830bf53fd93626638efc8fbb9f2374f90aedbf2c11ac4254c3f2a41634fc8bca710e80a2ac1c16ad41a1ea02aa55a058ab26608ee0a031ac17269c002ae7a8019b138360bcf1ab993a4b5ac3f60f7a9afa08d753f1cc30bddc418a446fa838889af02cd9ccc6468240d2600817306083aebe481694fb3408c5ec825d61c4f58f873d8b52d18a4252a822eb6c3ac8917a957ebbf2bac9a283ee6962a098a3cc035ceed16a9c1780bfb881f410fc6646e60b20a72f83bea18f9c15059e1b24ec0c021f8806f80a3908f10ddb0e6e462dace7e6a294ca0b9458778af0631c10dd126b8db71a2ce388a1f5c47ae258a9f1c037b29f5e38716e998a59e0081792d40062f867e00aa44eda5c655abef6a832fee80faf82fd42115a92e96ca8e6f4be687904960fbc6488e46870f16ea04d4e73a29f16cd1e5c0371cf5eef7f4f2257cf3cb3a4ee641c852274ed8c17c87ec1ccea9a8d38c08a5d8c884f028120d9fce60c716f60c2279f68710c501806afc83deeb00859dea3cba54572d4d4192d0f3bea769e78f3e00c16ae84baf9872da2e10851178e56ac8917300adfb87250999461403cacaa9d8d0f1cdcc6a8b08a6259f3b033312bddae75298af206da891aa4ce553272a32ad20fc76ce6ba35092fc011c76bebb4417dfd8103697c9496966890876269f3b033312498dcfeb0b38dfce96aac8be404374dbe50ab856ed640bfc9204d4ee83600e5555d4239fc848e85ccef3a24d9b4e0ba1d8c94087d64c8cccec243f5f89303a367f49bba91e334359c01dbe8e257e120d7e0a4c8d89945766b63261150ef6149b2c83593c8864464b93a88d7ec346c01bc19d0d0c6dea1296dced41e4917370670cd6f06afa492af62d87a1f4065e968a550dd43563761ba6bf7242ee4a624fe48b8cd1ca6c26bc0970620634ea0c9821b92837ba72ba5e1cd109da258475d300c58edc1ea6745216510b3225bc9ca5ccfced30c75d00dae7d145d02986ced10972cc23da967f8978fa211ce63e603c05b37e9f5fbe2242194dee9fd5c40d75309ec7fb1da50283992cf6ed36425f9409843b21e57d61e68801143723adc658c40c4db0b8b80a16f7338ceb05a98a750791f89b1c5a57092a294ad03cce2ea173490d4f01fae484b8bfc3018ac6724fc7cda5feaabc74c38ae0df2e81f4817411c4ce68882397c9a0fc4d0a4429cf70f66acfd2acd8b19f1cc9e5928728107e1313691315dd159444a543238f9949ebe217cc5e0f939a7d1512c107b0cecee320fddbd01555c144e4699b10842900d7a5413219e660cb0ef328e179e34eb58354bed23ec145a0'[1520:]