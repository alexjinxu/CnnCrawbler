# coding: utf-8

import codecs
from urllib import request, parse
from bs4 import BeautifulSoup
import re
import time
from urllib.error import HTTPError, URLError
import sys


###news data defination
class News(object):
    def __init__(self):
        self.url = None  # news' url
        self.topic = None  # news' topic
        self.date = None  # date
        self.content = None  # news' content
        self.author = None  # news' author
        self.keywords = None  # news' author
        self.description = None  # news' author



def getNews(url):

    print(url)
    html = request.urlopen(url).read().decode('utf-8', 'ignore')

    soup = BeautifulSoup(html, 'html.parser')

    if not (soup.find('section', {'id': 'body-text'})):
        print("AAAA")
        return


    news = News()  # create news object

    news.author = (soup.find('meta', {'itemprop': 'author'})).attrs['content']
    print(news.author)
    news.topic = (soup.find('meta', {'itemprop': 'headline'})).attrs['content']
    print(news.topic)
    news.date = (soup.find('meta', {'itemprop': 'datePublished'})).attrs['content']
    print(news.date)
    news.description = (soup.find('meta', {'itemprop': 'description'})).attrs['content']
    print(news.description)
    news.keywords = (soup.find('meta', {'itemprop': 'keywords'})).attrs['content']

    news.url = (soup.find('meta', {'itemprop': 'url'})).attrs['content']


    content = ''
    for i in soup.find_all('div', {'class': 'zn-body__paragraph'}):
       content = content + i.get_text()



    news.content = content


    f.write("-----------------------------------------"+"\n")
    f.write("time: " + news.date + "\n")
    f.write("url: " + news.url + "\n")
    f.write("author: " + news.author + "\n")
    f.write("headline: " + news.topic + "\n")
    f.write("description : " + news.description + "\n")
    f.write("keywords : " + news.keywords + "\n")
    f.write("content: " + news.content + "\n")


##dfs regression ###
def dfs(url):
    global count
    print(url)

    #################################################################
    # the is specific for CNN website rule
    # if need to grip other news website need adapt these rules
    ##################################################################
    #pattern1 = '\/(2020|2019)\/[0-9]{2}\/[0-9]{2}\/[a-z]{3,8}\/[a-z0-9_-]*\/index.html$'  # decoding in for cnn
    #pattern1 = '\/(2020|2019)\/[0-9]{2}\/[0-9]{2}\/(business|tech|sucess)\/[a-z0-9_-]*\/index.html$'  # decoding in webpage url for cnn
    pattern1 = '\/2020\/[0-9]{2}\/[0-9]{2}\/(business|tech|sucess)\/[a-z0-9_-]*\/index.html$'  # decoding in webpage url for cnn
    #pattern2 = 'https://www\.cnn\.com\/[0-9]{4}\/[0-9]{2}\/[0-9]{2}\/[a-z]{3,8}\/[a-z0-9_-]*\/index.html$'  # decoding rule for cnn
    #pattern2 = 'https://www\.cnn\.com\/(2020|2019)\/[0-9]{2}\/[0-9]{2}\/[a-z]{3,8}\/[a-z0-9_-]*\/index.html$' # decode the url in webpage for cnn
    #pattern2 = 'https://www\.cnn\.com\/(2020|2019)\/[0-9]{2}\/[0-9]{2}\/business|tech|sucess\/[a-z0-9_-]*\/index.html$'  # decode the url in web page for cnn
    pattern2 = '(https|http)://(www|edition)\.cnn\.com\/2020\/[0-9]{2}\/[0-9]{2}\/business|tech|sucess\/[a-z0-9_-]*\/index.html$'  # decode the url in web page for cnn


    # if url has visited then directly return
    if url in visited:  return
    #print(url)


    # add the url in visited queue for record
    visited.add(url)


    try:
        # for new rul make progress
        html = request.urlopen(url).read().decode('utf-8', 'ignore')

        soup = BeautifulSoup(html, 'html.parser')
        #print(url)
        if re.match(pattern2, url):

            getNews(url)


        ####extract the linkage in the web page####
        links = soup.findAll('a', href=re.compile(pattern1))

        for link in links:
            #print(link['href'])
            s = link['href']

            if s.find("http") == -1:
               s = "https://www.cnn.com" + link['href']

            if s not in visited:
               dfs(s)
            # count += 1
    except URLError as e:
        print(e)
        return
    except HTTPError as e:
        print(e)
        return


# print(count)
# if count > 3: return

visited = set()

# write the news'object into txt file
f = open('cnn/cnnNews.txt', 'a+', encoding='utf-8')

dfs('https://www.cnn.com/business/')
