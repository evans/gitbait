#summy
#from __future__ import absolute_import
#from __future__ import division, print_function, unicode_literals
#from sumy.parsers.html import HtmlParser
#from sumy.parsers.plaintext import PlaintextParser
#from sumy.nlp.tokenizers import Tokenizer
#from sumy.summarizers.lsa import LsaSummarizer as Summarizer
#from sumy.nlp.stemmers import Stemmer
#from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 1

from bs4 import BeautifulSoup
import urllib2
import json
import subprocess
import re
import os.path

from summarize import summarize


ss = summarize.SimpleSummarizer()

"""
Untracked files
git ls-files --others --exclude-standard
Modified files
git diff --name-only
"""
c_extensions = ['.h', '.c'];
py_extensions = ['.py'];

proc = subprocess.Popen(["git ls-files --others --exclude-standard"], stdout=subprocess.PIPE, shell=True)
(untracked, err) = proc.communicate()
#print "untracked:", untracked
proc = subprocess.Popen(["git diff --name-only"], stdout=subprocess.PIPE, shell=True)
(modified, err) = proc.communicate()
#print "modified:", modified

def get_comments(cmd, strip):
    comments = ""
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (raw_comments, err) = proc.communicate()
    for line in re.sub(strip, '', raw_comments).split('\n'):
        stripped = line.lstrip()
        if stripped:
            comments += stripped + '\n' + ''
    #print comments
    return comments

def generate_summary(filename):
    perl_cmd_c_comments = "perl -e \"$/=undef;print<>=~/((?:\/\*(?:[^*]|(?:\*+[^*\/]))*\*+\/)|(?:\/\/.*))/g;\" "
    makefile_comments = "grep \"^\s*[#\;]\|^\s*$\" "
    extension = os.path.splitext(filename)[1]
    comments = "trollolol get wrecked."

    if extension in c_extensions:
        comments = get_comments(perl_cmd_c_comments + filename, '[/*]')
    elif filename.endswith("Makefile"):
        comments = get_comments(makefile_comments + filename, '[#]')
    else:
        if os.path.isfile(filename):
            with open(filename, 'r') as fd:
                    comments = fd.read()

    #print comments
    #print filename
    #print ss.summarize(comments, 1)
    #print ss.summarize(comments, 1)
    return (ss.summarize(comments, 1), ss.summarize(comments, 3))



def add_and_commit(file_list):
    git_add = "git add "
    git_commit = "git commit -m "
    for fname in file_list.split('\n'):
        if fname:
            (summary, description) = generate_summary(fname)
            try:
                git_add_cmd = git_add + fname
                print git_add_cmd
                proc = subprocess.call(git_add_cmd, shell=True)

                git_commit_cmd = git_commit + "\"" + summary.replace('"', r'\"') + "\n\n" + description.replace('"', r'\"') + "\""
                print git_commit_cmd
                proc = subprocess.call(git_commit_cmd, shell=True)

            except subprocess.CalledProcessError as e:
                print (e)

add_and_commit(untracked)
add_and_commit(modified)
