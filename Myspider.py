#coding:utf8

from bs4 import BeautifulSoup

import re

import urlparse

import urllib2

import os

import sys

reload(sys)

sys.setdefaultencoding('utf-8')  # @UndefinedVariable




class UrlManager(object):

    def __init__(self):

        self.new_urls = set()

        self.old_urls = set()


 

    def add_new_url(self,url):

        if url is None:

            raise Exception 

        if url not in self.new_urls and url not in self.old_urls:

            self.new_urls.add(url)

 

    def add_new_urls(self,urls):

        if urls is None or len(urls) == 0:

            raise Exception 

        for url in urls:

            self.add_new_url(url)

 

    def has_new_url(self):

        return len(self.new_urls) != 0

 

    def get_new_url(self):

        new_url = self.new_urls.pop()

        self.old_urls.add(new_url)

        return new_url



class HtmlDownloader(object):

    def download(self, url):

        if url is None:

            return None

        response = urllib2.urlopen(url)

 

        if response.getcode() != 200:

            return None

        return response.read()


class HtmlParser(object):

    def _get_new_urls(self,page_url,soup):

        new_urls = []   

      

        links = soup.find_all("a",href=re.compile(r"/item/\w"))

        for link in links:

            new_url = link["href"]

            

            new_full_url =urlparse.urljoin(page_url,new_url)

            new_urls.append(new_full_url)

        return new_urls

 

    def _get_new_data(self,page_url,soup):

        res_data = {}

        #url

        res_data["url"] = page_url

        #<ddclass="lemmaWgt-lemmaTitle-title"><h1>Python</h1>

        title_node =soup.find("dd",class_="lemmaWgt-lemmaTitle-title").find("h1")
            
        res_data["title"] =title_node.get_text()

        #<divclass="lemma-summary" label-module="lemmaSummary">

        summery_node =soup.find("div",class_="para")

        res_data["summary"] =summery_node.get_text()

        return res_data

 

    def parse(self,page_url,html_cont):

        if page_url is None or html_cont is None:

            return

        soup = BeautifulSoup(html_cont,"html.parser", from_encoding="utf-8")

        new_urls = self._get_new_urls(page_url,soup)

        new_data = self._get_new_data(page_url,soup)

        return new_urls, new_data

 



class HtmlOutputer():

    def __init__(self):

        self.datas = []

 

    def collect_data(self, data):

        if data is None:

            return

        self.datas.append(data)

 

    def output_html(self):
        fout = open('output.html','w')

        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')

        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'])
            fout.write('<td>%s</td>' % data['summary'])
            fout.write('</tr>')

        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')

        fout.close()
    

 


class SpiderMain():

    def craw(self, root_url, page_counts):

        count = 1   

        UrlManager.add_new_url(root_url)

        while UrlManager.has_new_url():    

            try:

                

                new_url =UrlManager.get_new_url()

                

                print "\n crawed %d :%s" % (count, new_url)

                

                html_cont =HtmlDownloader.download(new_url)

                

                new_urls, new_data =HtmlParser.parse(new_url, html_cont)

                

                UrlManager.add_new_urls(new_urls)

                

                HtmlOutputer.collect_data(new_data)

 

               

                if count == page_counts:

                    break

                count = count + 1

            except:

                print "craw failed"

 

        

        HtmlOutputer.output_html()

 

if __name__=="__main__":

    print "\n Welcome to use spider:)"

   

    UrlManager = UrlManager()

    HtmlDownloader = HtmlDownloader()

    HtmlParser = HtmlParser()

    HtmlOutputer = HtmlOutputer()

 

    root_url = 'https://baike.baidu.com/item/%E8%90%9D%E8%8E%89/41169?fr=aladdin'  

    page_counts = input("Enter you want to craw how many pages:" ) 

 

    SpiderMain = SpiderMain()

    SpiderMain.craw(root_url,page_counts)   