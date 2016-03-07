#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
from cookielib import CookieJar
import json
import base64

def log_in(query):
    # Parse mail and password
	data_auth = query.split(" ")
	email = data_auth[0]
	password = data_auth[1]

    # Try log in to lingualeo
	try:
		auth = {'email': email, 'password': password}
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		response = opener.open("http://api.lingualeo.com/api/login", urllib.urlencode(auth))
		try_log_in = json.loads(response.read())

        # If data are correct momorize it. If not throw an error
		if not "error_code" in try_log_in:
			data = email+"||"+password
			with open('data', 'w') as database:
				database.write(base64.b64encode(data))
			return "You have successfully logged in"
		else:
			return "Error! Cannot log in to lingualeo. Check your e-mail and password"
	except Exception as e:
		print "ERROR: Cannot log in or write to file"
