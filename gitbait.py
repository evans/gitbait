from bs4 import BeautifulSoup
import urllib2
import json

page = urllib2.urlopen('http://www.buzzfeed.com/api/v2/feeds/index').read()
soup = BeautifulSoup(page, 'html.parser')

#print(soup.prettify())
full = json.loads(page)
print type(full['big_stories'])
print type(full['big_stories'][0])
print full.keys()
for article in full['big_stories']:
    print article['title']
for article in full['buzzes']:
    print article['title']
