from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import requests
import nltk
import gnp
import codecs
import json

# nltk.download() need to run this first time you use ntlk

URL = 'https://www.google.com/search?cf=all&hl=en&pz=1&ned=us&tbm=nws&gl=us&as_epq=Americas%20Barometer&as_occt=any&as_drrb=b&as_mindate=11%2F1%2F2015&as_maxdate=11%2F11%2F2015&tbs=cdr%3A1%2Ccd_min%3A11%2F1%2F2015%2Ccd_max%3A11%2F11%2F2015&authuser=0'

def run(**params):
    response = requests.get(URL.format(**params))
    soup = BeautifulSoup(response.text)
    print soup.prettify


list_queries = ["Latin American Public Opinion Project", "Americas Barometer", "El Proyecto de Opinion Publica de America Latina"]
for query in list_queries:
    print query
    print ""
    a = gnp.get_google_news_query(query)
    for key, value in a.iteritems():
        for item in value:
            try:
                snip = item.get('content_snippet')
                title = item.get('title')
                link = item.get('link', item.get('link'))
                print title
                print snip
                print link
            except:
                continue
            # print link
