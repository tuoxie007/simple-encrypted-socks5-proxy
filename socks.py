#! /usr/bin/python
# coding:utf-8
#
# File: socks.py
# Created: 2011-11-20
# Author: Xu Ke
# Email: tuoxie007@gmail.com
#

__author__ = 'xuke'


import socket, traceback, select
from toolkit import *

'''define statics'''
SOCKS_VER5 = '\x05'
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

timeout=10

def accept(cc, encrypted=False):
    '''\
cc: client connection

reply_client and connect to up server if needed,
and return the up connection,return False if client
request is invalid or exception cathed
'''
    try:
        cc = select.select([cc], [], [])[0][0]
        
        timeout = cc.gettimeout()
        cc.settimeout(timeout)

        # import pdb; pdb.set_trace()
        socks_version = cc.recv(1)
        method_number = cc.recv(1)
        if encrypted:
            method_number = xor(method_number)
        method_number = ord(method_number)
        methods_client_supported = ''
        for i in range(method_number):
            if encrypted:
                methods_client_supported += xor(cc.recv(1))
            else:
                methods_client_supported += cc.recv(1)
        #read over

        if encrypted:
            cc.sendall(xor(SOCKS_VER5+METHOD_NO_AUTHENTICATION_REQUIRED))
        else:
            cc.sendall(SOCKS_VER5+METHOD_NO_AUTHENTICATION_REQUIRED)
        #reply over

        socks_version = cc.recv(1)
        command = cc.recv(1)
        rsv = cc.recv(1)
        address_type = cc.recv(1)
        if encrypted:
            address_type = xor(address_type)
        if address_type == ATYP_DOMAINNAME:
            domain_length = cc.recv(1)
            if encrypted:
                domain_length = xor(domain_length)
            domain = cc.recv(ord(domain_length))
            if encrypted:
                domain = xor(domain)
            hostname = domain
            port = cc.recv(2)
            if encrypted:
                port = xor(port)
        elif address_type == ATYP_IPV4:
            domain_length = ''
            domain = cc.recv(4)
            if encrypted:
                domain = xor(domain)
            hostname = '%s.%s.%s.%s' % (str(ord(domain[0])), str(ord(domain[1])), str(ord(domain[2])), str(ord(domain[3])))
            port = cc.recv(2)
            if encrypted:
                port = xor(port)
        else:
            return False
         #read command over
        cc.settimeout(timeout)
        return ((hostname, ordlong(port)), {
                    'address_type': address_type,
                    'domain_length': domain_length,
                    'domain': domain,
                    'port': port
                })
    except:
        return False

def reply(cc, address, encrypted=False, connected=True):
    '''\
(connection, address, connected)
    '''
    try:
        timeout = cc.gettimeout()
        cc.settimeout(timeout)
        if connected: # reply for succss
            data = SOCKS_VER5\
                   +REP_succeeded\
                   +RSV\
                   +address['address_type']\
                   +address['domain_length']\
                   +address['domain']\
                   +address['port']
            if encrypted:
                data = xor(data)
            cc.sendall(data)
        else: # reply for failed
            data = SOCKS_VER5 + REP_Network_unreachable
            if encrypted:
                data = xor(data)
            cc.sendall(data)
        cc.settimeout(timeout)
        return True
    except:
        return False
