#!/usr/bin/env python
import web
import re
import base64
import json

#To Start web server: sudo python rest.py 8085
from feeder import Feeder

urls = (
    '/feed', 'feed_cats',
    '/time', 'get_time'

)

app = web.application(urls, globals())

allowed = (
	('user','pass'),
)

class get_time:
   def POST(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False

        if auth is None:
            authreq = True
        else:
                auth = re.sub('^Basic ','',auth)
                username,password = base64.decodestring(auth).split(':')
                if (username,password) in allowed:
	                web.header('Content-Type', 'application/json')
                        jsonResponse = {'date':Feeder.getDate()}
                        return json.dumps(jsonResponse)
                else:
                        authreq = True

        if authreq:
            web.header('WWW-Authenticate','Basic realm="Cat Feeder"')
            web.ctx.status = '401 Unauthorized'
            return

class feed_cats:
    def POST(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False

        if auth is None:
            authreq = True
        else:
            	auth = re.sub('^Basic ','',auth)
		username,password = base64.decodestring(auth).split(':')
            	
		if (username,password) in allowed:
			web.header('Content-Type', 'application/json')
			data = json.loads(web.data())
			feedTime = data["time"]
			feed = Feeder(float(feedTime))
			result = feed.feed()
			successDate = feed.getDate()
			jsonResponse = {'result':result,'date':successDate}
			return json.dumps(jsonResponse)
		else:
			authreq = True

        if authreq:
            web.header('WWW-Authenticate','Basic realm="Cat Feeder"')
            web.ctx.status = '401 Unauthorized'
            return

if __name__ == "__main__":
    import os, sys
    pid = os.fork()
    if pid is 0:
        sys.stdout = open('out.txt', 'w')
        sys.stderr = open('err.txt', 'w')
        app.run()
    else:
        print "Server forked off with pid of: %d" % pid 
