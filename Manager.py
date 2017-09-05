import requests
import logging
import multiprocessing
import threading
import os
import queue

from time import sleep
from ProcessLog import Listener
from CrawlConfig import CrawlConfig
from ContextDealer import ContextDealer
from UrlGenerator import UrlGenerator
from CrawlerThread import CrawlerThread

from threading import Thread
from multiprocessing import Event
from pybloom_live import BloomFilter


class Manager(CrawlConfig):
    def __init__(self, mark, markers):
        super().__init__()
        self.mark = mark
        self.dirty_urls = BloomFilter(self.max_urls, self.err_rate)
        self.markers = markers

        self.record_queue = multiprocessing.Queue()
        self.file_lock = multiprocessing.Lock()
        self.bloom_lock = threading.Lock()
        self.crawl_event = Event()
        self.file_cnt = multiprocessing.Value('i')
        self.file_cnt.value = 1
        self.content_queue = multiprocessing.Queue()
        self.url_queue = queue.Queue()
        self.dealers = []
        self.crawlers = []

        self.log_config(self.record_queue)
        self.listener = Listener(record_queue=self.record_queue)
        if os.path.exists('crawler.log'):
            os.remove('crawler.log')

    def start(self):
        self.listener.start()
        self.run_net_inspector()
        self.run_dealer()
        self.run_crawler()
        self.run_getter()

        self.url_getter.join()
        for i in range(self.max_thread):
            self.url_queue.put(None)
        for p in self.crawlers:
            p.join()
        for i in range(self.max_process):
            self.content_queue.put(None)
        for t in self.dealers:
            t.join()

        self.record_queue.put(None)
        self.listener.join()

    def run_dealer(self):
        for i in range(self.max_process):
            dealer = ContextDealer(content_queue=self.content_queue, file_cnt=self.file_cnt,
                                   crawl_event=self.crawl_event, file_lock=self.file_lock,
                                   mark=self.mark, markers=self.markers,
                                   record_queue=self.record_queue)
            self.dealers.append(dealer)
            dealer.start()

    def run_crawler(self):
        for i in range(self.max_thread):
            crawler = CrawlerThread(content_queue=self.content_queue, crawl_event=self.crawl_event,
                                    url_queue=self.url_queue, bloom_lock=self.bloom_lock, dirty_urls=self.dirty_urls)
            self.crawlers.append(crawler)
            crawler.start()

    def run_getter(self):
        self.url_getter = UrlGenerator(keywords=self.markers, url_queue=self.url_queue,
                                       crawl_event=self.crawl_event)
        self.url_getter.start()

    def inspect_net(self):
        while True:
            try:
                requests.get("http://www.baidu.com", timeout=self.timeout)
                self.crawl_event.set()
                logging.info("网络正常")
            except TimeoutError:
                logging.warning("网络超时")
            except Exception as e:
                logging.warning("网络异常 : " + str(type(e)))
            sleep(self.check_interval)

    def run_net_inspector(self):
        t = Thread(target=self.inspect_net)
        t.setDaemon(True)
        t.start()
