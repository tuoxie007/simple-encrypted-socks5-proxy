## Usage:

### Config your server host and/or port in the local.py.
Change address in the config.py

```
server_bind_addr = ("0.0.0.0", 3030)
local_bind_addr = ("127.0.0.1", 7070)

server_proxy_addr = ("your_remote_proxy_ip", server_bind_addr[1])
```

### Avoid hacks using your server
Change the encode function in the config.py, change ^200 to another value(0~255). Or your can change the encrypt arithmetic, such as ^20^30

### Run local.py on your local machine

	./local.py

### Run server.py on your remote server

	./server.py

### Set your the proxy config for applications
Select hostname, port and sock5 type.

Then end.
