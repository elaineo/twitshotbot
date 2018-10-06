import imgkit
import urllib.request
from bs4 import BeautifulSoup
import sys, logging, traceback

def screenshot(twit_url, twit_id):
	options = {
	    'encoding': "UTF-8",
	    'javascript-delay': '1000',
	    'crop-h': 600,
	    'xvfb': ''
	}
	imgfile = twit_id + '.png'
	
	try:
		f = urllib.request.urlopen(twit_url) 
		page = BeautifulSoup(f, 'html.parser')
		tweet = page.find("div", class_="permalink-tweet")
		if tweet:
			head = page.head
			css_hack = BeautifulSoup("<style>.icon { background: transparent }</style>", "html.parser")
			head.append(css_hack)
			imgkit.from_string(str(head) + str(tweet), imgfile, options=options)
		else:
			imgkit.from_url(twit_url, imgfile, options=options)
	except Exception as e:
		logging.debug(traceback.format_exception(*sys.exc_info()))
		return str(e)
	return imgfile