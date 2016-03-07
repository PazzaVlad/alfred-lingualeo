#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
from cookielib import CookieJar
import base64
import os
import time
import feedback
import sys
from random import randint


query = str(sys.argv[1])


def check_cache():
    if os.path.isfile('tmp/dict.json'):
        current_time = time.time()
        time_of_changing_file = os.path.getmtime('tmp/dict.json')
        difference = int(current_time - time_of_changing_file)
        if difference > 300:
            set_cache(auth_to_lingualeo())
            output_words()
        else:
            output_words()
    else:
        set_cache(auth_to_lingualeo())
        output_words()


def auth_to_lingualeo():
    # Check if you log in to lingualeo.com and can add words
    with open('data', "r") as data_file:
        auth_data = data_file.read()
    if len(auth_data) < 1:
        fb = feedback.Feedback()
        fb.add_item(title= "You are not logged in to Lingualeo!", subtitle="")
        print fb
        sys.exit()

    # Loggin in
    auth_data_split = base64.b64decode(auth_data).split("||")
    mail = auth_data_split[0]
    password = auth_data_split[1]
    auth = {'email': mail, 'password': password}
    try:
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.open("http://api.lingualeo.com/api/login", urllib.urlencode(auth))
    except Exception as e:
        return "ERROR: Cannot log in to lingualeo!"
    return opener


def set_cache(opener):
    response = opener.open("http://lingualeo.com/ru/userdict/json")
    with open("tmp/dict.json", "wb") as dict:
        dict.write(str(response.read()))

    json_from_file = open("tmp/dict.json")
    data = json.loads(json_from_file.read())

    for item in data["userdict3"]:
        for word in item["words"]:
            if word["picture_url"]:
                picture = 'http:' + word["picture_url"]
                img_name = picture.split('/')[-1]
                img_folder = r'tmp/img/'
                img_path = img_folder + img_name
                if not os.path.isfile(img_path):
                    f = open(img_path,'wb')
                    f.write(urllib.urlopen(picture).read())
                    f.close()



def parse_words():
    json_from_file = open("tmp/dict.json")
    data = json.loads(json_from_file.read())

    dictionary = []
    for item in data["userdict3"]:
        for word in item["words"]:
            card = {}
            card['word'] = word["word_value"]
            card['translations'] = ""
            for trns in word["user_translates"]:
                card['translations'] += trns["translate_value"]
            picture = word["picture_url"]
            if picture:
                img_name = picture.split('/')[-1]
                img_folder = r'tmp/img/'
                card['img_path'] = img_folder + img_name
            else:
                card['img_path'] = 'default.png'
            card['context'] = word["context"]
            card['title'] = card['word'].upper() + " - " + card['translations']
            dictionary.append(card)
    return dictionary


def output_words():
    dictionary = parse_words()
    fb = feedback.Feedback()

    if query == "w":
        for card in dictionary[0:50]:
            if card['word'].strip().find(' ') == -1:
                fb.add_item(title=card['title'], subtitle=card['context'], icon=card['img_path'], arg=card['word'])

    elif query == "p":
        for card in dictionary[0:50]:
            if card['word'].strip().find(' ') != -1:
                fb.add_item(title=card['title'], subtitle=card['context'], icon=card['img_path'], arg=card['word'])

    elif query == "r":
        max_number = len(dictionary) - 1
        random_number = randint(0,max_number)
        title = dictionary[random_number]['title']
        subtitle = dictionary[random_number]['context']
        icon = dictionary[random_number]['img_path']
        arg = dictionary[random_number]['word']
        fb.add_item(title=title, subtitle=subtitle, icon=icon, arg=arg)

    else:
        for card in dictionary[0:50]:
            fb.add_item(title=card['title'], subtitle=card['context'], icon=card['img_path'], arg=card['word'])

    print fb

if __name__ == "__main__":
    check_cache()
