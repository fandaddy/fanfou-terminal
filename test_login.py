#!usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup
from termcolor import colored, cprint

def cls():
    print '\n' * 100

cls

url = 'http://fanfou.com/login?fr=%2Flogin'
url_l = 'http://fanfou.com/login'
url_home = 'http://m.fanfou.com/home'
url_next = 'http://m.fanfou.com/home/p.2'

headers_get = {
    'Host': 'fanfou.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Referer': 'http://fanfou.com/',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }

headers_login = {
    'Host': 'fanfou.com',
    'Connection': 'keep-alive',
    'Content-Length': '163',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://fanfou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Referer': 'http://fanfou.com/',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }

s = requests.session()
r = s.get(url, headers=headers_get)
action = BeautifulSoup(r.content, "lxml").find('input', attrs={'name':'action'})['value']
token = BeautifulSoup(r.content, "lxml").find('input', attrs={'name':'token'})['value']
urlfrom = BeautifulSoup(r.content, "lxml").find('input', attrs={'name':'urlfrom'})['value']
login_data = {
    'loginname':'*******@******',        #填写你的用户名
    'loginpass':'',           #填写你的密码
    'action':action,
    'token':token,
    'urlfrom':urlfrom
    }

res = s.post(url, data=login_data, headers=headers_login)
res_home = s.get(url_home)
soup = BeautifulSoup(res_home.content, "lxml")
cprint(soup.title.string, 'white', 'on_blue')
print

timelines = soup.findAll('p')
count = 1
for timeline in timelines:
    author = timeline.find('a', class_='p')
    if author != None:
        cprint(author.text, 'yellow')
        #print timeline
        timesent = timeline.find('span', class_='t')

        i = 1
        former = None
        seg2 = None
        cont = None
        tr_cont = None
        for seg in timeline:
            if i == 2:
                seg2 = seg
                #print i,seg2
            if i == 3 and seg.text == '':
                cont = seg2
            elif i == 3 and seg.text != '':
                #print i, seg
                tr_cont = seg2
                former = seg.text
            if i == 4 and tr_cont != None:
                cont = seg
                #print i,cont
            if i == 5:
                break
            i = i + 1
        #print "tr_cont"+tr_cont    
        if tr_cont == None:
            print cont
        else:
            print tr_cont, former
            #cprint(tr_cont, 'red')
            print cont
        cprint(timesent.text, 'blue')
        cprint('################################################################################################', 'magenta')
        count15 = 0
    if count == 9 or count == 15:
        print "‘p’：看更多, 'n'：结束"
        if count == 15:
            count15 = count15 + 1
        page_key = raw_input()
        if page_key == 'p':
            cls()
        elif page_key == 'n':
            break
    count = count + 1

s.get(url)
