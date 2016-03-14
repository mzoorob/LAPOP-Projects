from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import requests
import gnp
import excerpt_extractor
import re
import codecs
import time
import unicodedata
import numpy
from pygoogle import pygoogle


def scrape_link(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})
    soup = BeautifulSoup(response.text, "lxml")
    soup = cleanSoup(soup)
    text = soup.get_text
    print text
    #  = unicodedata.normalize('NFKD', soup).encode('ascii','ignore')
    # print text
    return

def cleanSoup(soup):
    # get rid of javascript, noscript and css
    [[tree.extract() for tree in soup(elem)] for elem in ('script','noscript','style')]
    # get rid of doctype
    subtree = soup.findAll(text=re.compile("DOCTYPE"))
    [tree.extract() for tree in subtree]
    # get rid of comments
    # comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    # [comment.extract() for comment in comments]
    return soup


def save_file(list, filename):
    file_stuff = open(filename, "w")
    for item in list:
        file_stuff.write(item)
        file_stuff.write("\n")


print excerpt_extractor.get_summary("http://www.worldpoliticsreview.com/articles/17167/growing-pains-urbanization-and-governance-in-peru")[1] + '\n'

list_content = []
list_queries = ["\"Latin American Public Opinion Project\"", "\"Latin America Public Opinion Project\"", "\"LAPOP\"", "\"Americas Barometer\"", "\"AmericasBarometer\"",
                "\"El Proyecto de Opinion Publica de America Latina\"", "\"Barometro de las Americas\"", "Elizabeth Zechmeister", "Elizabeth J Zechmeister", "\"Mitchell Seligson\""]
for query in list_queries:
    a = gnp.get_google_news_query(query)
    list_content.append(query)
    list_content.append("\n")
    for key, value in a.iteritems():
        for item in value:
            try:
                snip = item.get('content_snippet')
                title = item.get('title')
                link = item.get('link')
                list_content.append(snip)
                list_content.append(title)
                list_content.append(link)
                list_content.append("\n")
                # try:
                    # scrape_link(link)
                # except:
                    # print 'error'
                    # continue
            except:
                continue

save_file(list_content, "Lapop_News.txt")

for query in list_queries:
    g = pygoogle(query)
    g.pages = 1
    print '*Found %s results*'%(g.get_result_count())
    print g.get_urls()
    num = numpy.random.rand()*5
    print num
    time.sleep(num)
