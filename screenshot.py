# -*- coding: utf-8 -*-
from PIL import Image
from TwitterAPI import TwitterAPI

import imgkit
import urllib
from bs4 import BeautifulSoup

def screenshot(twit_url, twit_id):
	try:
		f = urllib.request.urlopen(twit_url) 
		page = BeautifulSoup(f, 'html.parser')
		head = page.head
		tweet = page.find("div", class_="permalink-tweet")

		css_hack = BeautifulSoup("<style>.icon { background: transparent }</style>", "html.parser")
		head.append(css_hack)

		options = {
		    'encoding': "UTF-8",
		    'javascript-delay': '1000',
		    "xvfb": ""
		}

		imgfile = twit_id + '.png'
		imgkit.from_string(str(head) + str(tweet), imgfile, options=options)
	except Exception as e:
		return str(e)
	return imgfile