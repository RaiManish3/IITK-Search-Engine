from urlparse import urlparse
import re
import json
from bs4 import BeautifulSoup
import scrapy
from scrapy.utils.markup import remove_tags

base_url = 'http://home.iitk.ac.in/~'
allusersFile = 'allUsers.txt'
resultsFile = 'scrapedData.json'
outFile=open(resultsFile,'w')
outFile.close()
outFile=open(resultsFile,'a')
auf = open(allusersFile,'r')

#do_not_visit_these = ['^#','facebook','linkedin','instagram','quora','twitter','google','youtube','void','oars','jpg','png','gif','pdf','mailto:','zip$','github.com','yahoo','flipkart','amazon','microsoft']
#DNVreg = r''+ '|'.join(do_not_visit_these)

## extend the allowed domains here
allowed_domains_defined = ['home.iitk.ac.in','www.iitk.ac.in','github.io']

def pageData(soup):
    texts = soup.findAll(text=True)

    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True

    visible_texts = filter(visible, texts)
    return ' '.join(' '.join(list(visible_texts)).splitlines())


def htmlText(soup):
    for script in soup.find_all('script'):
        script.extract()
    for style in soup.find_all('style'):
        style.extract()
    data = ' '.join(soup.get_text().strip().split())
    return data


class IITKSpider(scrapy.Spider):
    name = 'iitk_spider'
    start_urls = [(base_url+'{0}').format(i.strip()) for i in auf.readlines()]
    #start_urls += ['http://www.iitk.ac.in/']

    def parse(self, response):
       	try:
        	allText = ' '.join(response.xpath("//html").extract()).strip()
                soup = BeautifulSoup(allText,'html.parser')
                visibleText = htmlText(soup)
                outFile.write(json.dumps({"url":str(response.url),"pageData":str(visibleText)})+'\n')
        except:
        	print "Unable to parse"

        NEXT_PAGE_SELECTOR = 'a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract()
        for np in next_page:
            domainName = urlparse(response.urljoin(np)).netloc
            if domainName in allowed_domains_defined and 'pdf' not in response.urljoin(np) :
                try:
                    yield scrapy.Request(
                        response.urljoin(np),
                        callback=self.parse
                    )
                except:
                    print "Unable to crawl", str(response.urljoin(np))
