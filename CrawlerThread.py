import requests
import logging
from CrawlConfig import CrawlConfig
from threading import Thread


class CrawlerThread(Thread, CrawlConfig):
    def __init__(self, url_queue, content_queue, crawl_event, net_event, bloom_lock, dirty_urls):
        Thread.__init__(self)
        CrawlConfig.__init__(self)
        self.setDaemon(True)
        self.url_queue = url_queue
        self.crawl_event = crawl_event
        self.content_queue = content_queue
        self.bloom_lock = bloom_lock
        self.dirty_urls = dirty_urls
        self.net_event = net_event
        self.completed = False

    def run(self):
        while True:
            self.crawl()
            if self.completed:
                return

    def crawl(self):
        html = None
        try:
            url = self.url_queue.get()
            if url is None:
                self.completed = True
                return False
            html = requests.get(url, headers=self.randomheaders(),
                                timeout=self.timeout)

            self.bloom_lock.acquire()
            for ban_url in self.ban_urls:
                if ban_url in html.url:
                    logging.info("Banned : " + html.url)
                    self.bloom_lock.release()
                    return True
            if self.dirty_urls.add(html.url):
                logging.info("Dirty : " + html.url)
                self.bloom_lock.release()
                return True
            self.bloom_lock.release()

            logging.info("New : " + html.url)
            html.encoding = html.apparent_encoding
            self.content_queue.put(html.url + "$$$" + html.text)
            if self.content_queue.qsize() >= self.max_contents:
                logging.warning("Wait : content -  " + str(self.content_queue.qsize()) +
                                " > " + str(self.max_contents))
                self.crawl_event.clear()
                self.crawl_event.wait()
                logging.warning("Continue : content - " + str(self.content_queue.qsize()))
        except TimeoutError:
            logging.warning("TimeOut")
            self.net_event.clear()
            self.net_event.wait()
            logging.warning("Continue : TimeOut")
        except Exception as e:
            if html is None:
                logging.warning("Unknown Exception : " + str(type(e)) + " -  html is None")
            else:
                logging.warning("Unknown Exception : " + str(type(e)) + " - " + html.url)
        finally:
            return True
