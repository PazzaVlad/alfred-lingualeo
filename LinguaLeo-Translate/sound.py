#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import sys
from time import sleep

word = str(sys.argv[1])

# TODO: DRY!
def get_json(query):
	url = "http://api.lingualeo.com/gettranslates?word=" + query
	try:
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		return data
	except Exception as e:
		return "ERROR:Cannot translate this text!"


def sound_text(word):
	try:
		word = word.lower().strip()
		url = "https://ssl.gstatic.com/dictionary/static/sounds/de/0/"+word+".mp3"
		f = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		sleep(1)
		data = get_json(word)
		url = data["sound_url"]
		f = urllib2.urlopen(url)
	with open("tmp/sound.mp3", "wb") as code:
		code.write(f.read())


if __name__ == "__main__":
	sound_text(word)
