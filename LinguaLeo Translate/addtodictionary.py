#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
from cookielib import CookieJar

# https://github.com/relaxart/lingualeo.export - lingualeo API

def add_to_dictionary(query, mail, password):
	#Log in to lingualeo.com
	try:
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		auth = {'email': mail, 'password': password}
		response = opener.open("http://api.lingualeo.com/api/login", urllib.urlencode(auth))
	except Exception as e:
		return "ERROR:Cannot login to lingualeo!"

	# Parse english word and its translation from previous script
	words = query.split("||")
	word = words[0]
	tword = words[1]
	vocabulary = {"word" : word.lower(), "tword" : tword.lower()}

	# If word exist - add it to the dictionary
	response = opener.open("http://api.lingualeo.com/gettranslates?word=" + word)
	translated = json.loads(response.read())
	exist = int(translated["is_user"])
	if not (exist):
		response = opener.open("http://api.lingualeo.com/addword", urllib.urlencode(vocabulary))
		return words[0] + "\n" + words[1]
	else:
		return "This word is already in your dictionary!"
