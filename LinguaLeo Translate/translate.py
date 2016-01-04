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
		sorted_output = sorted(output, key=lambda student: int(student['votes']), reverse=True)
		fb = feedback.Feedback()
		
		for item in sorted_output:
			translation = item["value"]
			popularity = str(item["votes"])
			arguments = query+"||"+str(item["id"])
			fb.add_item(title=translation, subtitle=popularity, arg=arguments)
		return fb
	except Exception as e:
		return "ERROR:Cannot translate this text!"
