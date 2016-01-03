#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import feedback

def translate_text(query):
	# Translate word and output it to XML parser fro Alfred
	url = "http://api.lingualeo.com/gettranslates?word=" + query
	try:
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		output = data["translate"]
		fb = feedback.Feedback()
		for x in sorted(output, key=lambda student: int(student['votes']), reverse = True):
			fb.add_item(title=x["value"], subtitle=str(x["votes"]), arg=query +"||"+ x["value"])
		return fb
	except Exception as e:
		return "ERROR:Cannot translate this text!"
