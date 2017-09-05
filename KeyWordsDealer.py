import os
import json
from CrawlConfig import CrawlConfig


class KeyWordsDealer(CrawlConfig):
    def __init__(self):
        super().__init__()
        self.load_keyword_config()

    def load_keyword_config(self):
        with open(self.keyword_config, 'r', encoding='u8') as keyword_config_file:
            configs = json.load(keyword_config_file)
            self.min_keyword_length = configs["min-keyword-length"]
            self.max_keyword_length = configs["max-keyword-length"]
            self.keyword_file_dir = configs["keyword-file-dir"]
            self.keyword_file_ext = configs["keyword-file-ext"]
            self.keyword_mark_map = configs["keyword-mark-map"]
            self.mark = configs["mark"]

    def load_markers(self):
        self.marks = {}
        for filename in os.listdir(self.keyword_file_dir):
            if filename.endswith(self.keyword_file_ext):
                basename = filename[:filename.rfind('.')]
                in_file = open(filename, 'r', encoding='u8')
                for keyword in in_file:
                    self.marks[keyword] = self.keyword_mark_map[basename]





