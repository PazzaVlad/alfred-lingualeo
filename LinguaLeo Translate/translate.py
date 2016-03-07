#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import feedback
import sys


def get_json(query):
	url = "http://api.lingualeo.com/gettranslates?word=" + query
	try:
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		return data
	except Exception as e:
		return "ERROR:Cannot translate this text!"


# Take query from Alfred
word = str(sys.argv[1])
json_data = get_json(word)


def translate_text():
	# Translate word and output it to XML parser for Alfred
	data = json_data
	output = data["translate"]
	sorted_output = sorted(output, key=lambda student: int(student['votes']), reverse=True)

	fb = feedback.Feedback()
	for item in sorted_output:
		translation = item["value"]
		popularity = str(item["votes"])
		arguments = word+"||"+str(item["id"])
		fb.add_item(title= translation, subtitle=popularity, arg=arguments)
	return fb


print translate_text()
