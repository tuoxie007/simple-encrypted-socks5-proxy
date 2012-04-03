
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