from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import requests
import nltk
import gnp
import codecs
import json

# nltk.download() need to run this first time you use ntlk

# first = urllib2.urlopen("http://www.thelawmakers.org/#/research").read()
# soup = BeautifulSoup(first)


URL = 'https://www.google.com/search?cf=all&hl=en&pz=1&ned=us&tbm=nws&gl=us&as_epq=Americas%20Barometer&as_occt=any&as_drrb=b&as_mindate=11%2F1%2F2015&as_maxdate=11%2F11%2F2015&tbs=cdr%3A1%2Ccd_min%3A11%2F1%2F2015%2Ccd_max%3A11%2F11%2F2015&authuser=0'
BASE_URL = "http://genius.com"

def count_words(lyrics, word):
    list_words = nltk.word_tokenize(lyrics)
    count = 0
    real = 0
    idx = 0
    for lyric in list_words:
        if len(lyric)>2:
            real += 1
        if lyric == word:
            print lyric+" "+list_words[idx+1]
            if lyric+" "+list_words[idx+1] == "crack baby":
                count += 1
        idx += 1
    return float(count)/real*1000

def search_artist(artist_url):
    response = requests.get(artist_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})
    soup = BeautifulSoup(response.text, "lxml")
    for song_link in soup.select('ul.song_list > li > a'):
            link = urljoin(BASE_URL, song_link['href'])
            response = requests.get(link)
            soup = BeautifulSoup(response.text)
            print soup.title.string
            lyrics = soup.find('div', class_='lyrics').text.strip()
            print count_words(lyrics, "crack")
            for song_link in soup.select('ul.song_list > li > a'):
                link = urljoin(BASE_URL, song_link['href'])
                response = requests.get(link)
                soup = BeautifulSoup(response.text)
                print soup.title.string
                lyrics = soup.find('div', class_='lyrics').text.strip()
                print count_words(lyrics, "crack")

def run(**params):
    response = requests.get(URL.format(**params))
    soup = BeautifulSoup(response.text)
    print soup.prettify

# run(query="Lebanon", month=9, from_day=1, to_day=31, year=15)
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

# print "Kembe"
# search_artist("http://genius.com/artists/Kembe-x/")
# print "Isaiah"
# search_artist("http://genius.com/artists/Isaiah-Rashad/")

