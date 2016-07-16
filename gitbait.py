from bs4 import BeautifulSoup
import urllib2
import json
import subprocess

page = urllib2.urlopen('http://www.buzzfeed.com/api/v2/feeds/index').read()
soup = BeautifulSoup(page, 'html.parser')

#print(soup.prettify())
full = json.loads(page)
titles = []
#print type(full['big_stories'])
#print type(full['big_stories'][0])
#print full.keys()
for article in full['big_stories']:
    title = article['title']
    if not (title in titles):
        titles.append(title)
for article in full['buzzes']:
    title = article['title']
    if not (title in titles):
        titles.append(title)
title_iter = iter(titles)

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


def add_and_commit(file_list):
    git_add = "git add "
    git_commit = "git commit -m "
    for fname in file_list.split('\n'):
        if fname:
            try:
                git_add_cmd = git_add + fname
                proc = subprocess.call(git_add_cmd, shell=True)
                print git_add_cmd
                try:
                    message = next(title_iter)
                    if message:
                        git_commit_cmd = git_commit + "\"" + message + "\""
                        proc = subprocess.call(git_commit_cmd, shell=True)
                        print git_commit_cmd
                except StopIteration as e:
                    git_commit_cmd = git_commit + "\"lol jk get rekt\""
                    print git_commit_cmd
            except CalledProcessError as e:
                print e

add_and_commit(untracked)
add_and_commit(modified)
