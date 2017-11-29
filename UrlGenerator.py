import re
import requests
import logging
from threading import Thread
from CrawlConfig import CrawlConfig


class UrlGenerator(Thread, CrawlConfig):
    def __init__(self, keywords, hints, url_queue, net_event):
        CrawlConfig.__init__(self)
        Thread.__init__(self)
        self.keywords = keywords
        self.hints = hints
        self.url_queue = url_queue
        self.net_event = net_event

    def run(self):
        self.crawl()

    def crawl(self):
        for keyword in self.keywords:
            logging.info("Current keyword : " + keyword)
            
            for i in range(0, self.max_page * 10, 10):
                baidu_url = "http://www.baidu.com/s?wd=" + \
                            keyword + " " + self.hints[keyword] + "&pn=" + str(i)
                try:
                    html = requests.get(baidu_url, timeout=self.timeout)
                except:
                    logging.warning('Wait')

                    self.net_event.clear()
                    self.net_event.wait()

                    logging.warning('Continue')
                    self.net_event.clear()
                    i -= 1
                    continue

                urls = re.findall(
                    r'http://www.baidu.com/link\?url=[^"]+', html.text)
                urls = set(urls)
                for url in urls:
                    self.url_queue.put(url)