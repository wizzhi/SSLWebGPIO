#!/usr/bin/env python

from bottle import Bottle, get, post, request,response, run, ServerAdapter, route, hook
from time import sleep
from datetime import datetime
from collections import deque

startAt = str( datetime.now() )

# copied from bottle. Only changes are to import ssl and wrap the socket
class SSLWSGIRefServer(ServerAdapter):
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket (
        	srv.socket,
        	certfile='/root/web/cert.pem',  # path to certificate
        	keyfile='/root/web/key.unsec.pem',
        	server_side=True)
        srv.serve_forever()

log=deque(maxlen=2000)

@hook('after_request')
def my_log():
    log.appendleft(
        '%s [%s] %s %s %s' % (request.remote_addr,
                              datetime.now(),
                              request.method,
                              request.url,
                              response.status)
    )


@get('/x')
def display():
    return html()

@post('/x')
def doPost():
    password = request.forms.get('password')
    if password == 'd':
        openDoor()
    else:
        sleep(5)
    return html()

	
def html():
    return ( """
    <div>Last """ + str(len(log)) + " requests (up to 2000) since " + startAt + """</div>
    <Form action='/x' method='post'>
      <textarea rows='10' cols='60' wrap='off' readonly="readonly">""" +
      "\n".join(log) + """</textarea>
      </br>  
      <input name='password' type='password'></input>
      <input type='submit'>
    </form>""" )


def openDoor():
    from pyA20.gpio import gpio,port
    lock = port.PG7
    gpio.init()
    gpio.setcfg(lock, gpio.OUTPUT)
    gpio.output(lock, 1)
    sleep(0.3)
    gpio.output(lock, 0)


srv = SSLWSGIRefServer(host="0.0.0.0", port=9988)
run(server=srv)

