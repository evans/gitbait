from bs4 import BeautifulSoup
import urllib2
import json
import subprocess

unique_titles = []

top_keys = ['big_stories', 'buzzes']

def scrape_json(full_json):
    titles = []
    for key in top_keys:
        for article in full_json[key]:
            title = article['title']
            if not (title in unique_titles):
                unique_titles.append(title)
                titles.append(title)
    return titles

def scrape_extension(extension):
    print extension
    title = []
    base_url = 'http://www.buzzfeed.com/api/v2/feeds/'
    page = urllib2.urlopen(base_url + extension).read()
    #soup = BeautifulSoup(page, 'html.parser')

    #print(soup.prettify())
    full = json.loads(page)

    return iter(scrape_json(full))

    #print type(full['big_stories'])
    #print type(full['big_stories'][0])
    #print full.keys()


extensions = [  'index',

                'podcasts',
                'poitics',
                'puzzles',
                'reader',
                'rewind',
                'science',
                'sports',
                'style',
                'tech',
                'travel',
                'weddings',
                'weekends',
                'world',

                'lol',
                'win',
                'omg',
                'fail',
                'geeky',
                'life',
                'news',
                'videos',
                'music',
                'buzz',
                'parents',
                'audio',
                'celebrity',
                'entertainment',
                'lgbt',
                'books',
                'business',
                'quizzes',
                'animals',
                'diy',
                'food',
                'wtf']


extension_iter = iter(extensions)
title_iter = scrape_extension(next(extension_iter))
#print tuple(title_iter)

"""
Untracked files
git ls-files --others --exclude-standard
Modified files
git diff --name-only
"""

proc = subprocess.Popen(["git ls-files --others --exclude-standard"], stdout=subprocess.PIPE, shell=True)
(untracked, err) = proc.communicate()
#print "untracked:", untracked
proc = subprocess.Popen(["git diff --name-only"], stdout=subprocess.PIPE, shell=True)
(modified, err) = proc.communicate()
#print "modified:", modified


def add_and_commit(titles, file_list):
    git_add = "git add "
    git_commit = "git commit -m "
    for fname in file_list.split('\n'):
        if fname:
            try:
                git_add_cmd = git_add + fname
                #print git_add_cmd
                proc = subprocess.call(git_add_cmd, shell=True)
                message = ""
                try:
                    message = next(titles)
                except StopIteration as e:
                    while not message:
                        try:
                            titles = scrape_extension(next(extension_iter))
                            message = next(titles)
                        except StopIteration as e:
                            message = "lol jk get rekt"

                if message:
                    git_commit_cmd = git_commit + "\"" + message.replace('"', r'\"') + "\""
                    #print git_commit_cmd
                    proc = subprocess.call(git_commit_cmd, shell=True)

            except subprocess.CalledProcessError as e:
                print e

add_and_commit(title_iter, untracked)
add_and_commit(title_iter, modified)
