# SSLWebGPIO

1. install bottle:
```
$ wget https://bottlepy.org/bottle.py
```
2. generate SSL certificate:
```
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
```
3. update filepath, GPIO ports and password in run.py and run.
