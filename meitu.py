#coding=utf-8
import urllib2
import re
import Queue
import lxml
from bs4 import BeautifulSoup

num = 0
tieq = Queue.Queue()

#打开起始链接，识别其中的帖子链接
#百度贴吧中，帖子的链接class为j_th_tit 
def startScrap(url):
    # try:
    web = urllib2.urlopen(url)
    content = web.read()
    html = lxml.etree.HTML(content)
    result = html.xpath('//a[@class="j_th_tit "]')
    for u in result:
        tieurl = "https://tieba.baidu.com%s"%u.get('href')
        tieq.put(tieurl)
    while not tieq.empty():
        findimage(tieq.get())

#将发现的帖子链接传入，打开帖子后，识别其中的图片链接
#百度贴吧的中，帖子里的图片class属性为BDE_Image
def findimage(url):
    web = urllib2.urlopen(url)
    content = web.read()
    html = lxml.etree.HTML(content)
    result = html.xpath('//img[@class="BDE_Image"]')
    for u in result:
        picurl = u.get('src')
        downloadPic(picurl)

#将图片的链接地址传入，下载图片到指定文件中
def downloadPic(url):
    global num
    print "downloading:%s..."%url
    try:
        response = urllib2.urlopen(url)
        content = response.read()
    except Exception as e:
        print "downloading error reasion is:%s"%e.message
        return
    try:
        filename = "%d.%s"%(num,re.findall(r'(jpg| jpeg|JPG|JPEG|PNG|GIT|png|gif)+',url)[0])
        num+=1
        f = open(filename,"w")
        f.write(content)
    except IOError:
        print "file error"


starturl = 'https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%9B%BE&ie=utf-8'
startScrap(starturl)






