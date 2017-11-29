import json
import logging
import logging.handlers
from random import randrange

class CrawlConfig:
    def __init__(self, common_config_path=".\\common.json"):
        self.common_config_path = common_config_path
        self.common_config()

    def randomheaders(self):
        """生成随机请求头"""
        headers = {}
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Connection'] = 'keep-alive'
        headers['Cache-Control'] = 'max-age=0'
        headers['User-Agent'] = self.user_agents[randrange(len(self.user_agents))]
        return headers

    def common_config(self):
        with open(self.common_config_path, 'r', encoding='u8') as common_config_file:
            configs = json.load(common_config_file)
            self.ban_urls = configs["ban-urls"]
            self.user_agents = configs["user-agents"]
            self.max_thread = configs["max-thread"]
            self.max_process = configs["max-process"]
            self.max_contents = configs["max-contents"]
            self.min_contents = configs["min-contents"]
            self.min_marks = configs["min-marks"]
            self.max_urls = configs["max-urls"]
            self.err_rate = configs["err-rate"]
            self.max_page = configs["max-page"]
            self.check_net_interval = configs["check-net-interval"]
            self.check_queue_interval = configs["check-queue-interval"]
            self.timeout = configs["timeout"]
            self.keyword_config = configs["keyword-config"]
            self.TEXT_MARK = configs["TEXT-MARK"]
            self.DEL_MARK = configs["DEL-MARK"]

    def log_config(self, record_queue):
        h = logging.handlers.QueueHandler(record_queue)
        root = logging.getLogger()
        root.addHandler(h)
        root.setLevel(logging.INFO)
