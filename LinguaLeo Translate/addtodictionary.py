#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
from cookielib import CookieJar
import base64

# https://github.com/relaxart/lingualeo.export - lingualeo API

def add_to_dictionary(query):
	# Parse english word and translation's id from previous script
	data_from_alfred = query.split("||")
	eng_word = data_from_alfred[0]
	trans_id = data_from_alfred[1]

	# Check if you log in to lingualeo.com and can add words
	with open('data', "r") as data_file:
		auth_data = data_file.read()
	if len(auth_data) < 1:
		return "You are not logged in to Lingualeo"

	# Loggin in
	auth_data_split = base64.b64decode(auth_data).split("||")
	mail = auth_data_split[0]
	password = auth_data_split[1]
	auth = {'email': mail, 'password': password}
	try:
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		response = opener.open("http://api.lingualeo.com/api/login", urllib.urlencode(auth))
	except Exception as e:
		return "ERROR: Cannot log in to lingualeo!"

	# Get translation of the word
	response = opener.open("http://api.lingualeo.com/gettranslates?word=" + urllib.quote(eng_word))
	data_from_lingua = json.loads(response.read())

	# Find selected translation by ID
	finded_rus_word = ""
	for item in data_from_lingua['translate']:
		if int(trans_id) == int(item["id"]):
			finded_rus_word = item["value"]
	rus_word = finded_rus_word.encode('utf-8')
	vocabulary = {"word" : eng_word, "tword" : rus_word}

	# If word not exist - add it to the dictionary
	already_exist = data_from_lingua["is_user"]
	if not (already_exist):
		response = opener.open("http://api.lingualeo.com/addword", urllib.urlencode(vocabulary))
		return "Added: " + eng_word + " - " + rus_word
	else:
		return "This word is already in your dictionary!"
