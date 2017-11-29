import os
import json
from CrawlConfig import CrawlConfig


class KeyWordsDealer(CrawlConfig):
    def __init__(self):
        super().__init__()
        self.markers = {}
        self.hints = {}
        self.load_keyword_config()
        self.init_markers()
        self.filter_markers()

    def load_keyword_config(self):
        with open(self.keyword_config, 'r', encoding='u8') as keyword_config_file:
            configs = json.load(keyword_config_file)
            self.min_keyword_length = configs["min-keyword-length"]
            self.max_keyword_length = configs["max-keyword-length"]
            self.keyword_file_dir = configs["keyword-file-dir"]
            self.keyword_file_ext = configs["keyword-file-ext"]
            self.keyword_mark_map = configs["keyword-mark-map"]
            self.keyword_hint_map = configs["keyword-hint-map"]
            self.mark = configs["mark"]

    def init_markers(self):
        for filename in os.listdir(self.keyword_file_dir):
            if filename.endswith(self.keyword_file_ext):
                basename = filename[:filename.rfind('.')]
                in_file = open(os.path.join(self.keyword_file_dir, filename), 'r', encoding='u8')
                for keyword in in_file:
                    keyword = keyword.strip()
                    self.markers[keyword] = self.keyword_mark_map[basename]
                    self.hints[keyword] = self.keyword_hint_map[basename]

    def filter_markers(self):
        print("running filter。。。")
        s = ''.join(self.markers.keys())
        self.markers = \
            {k: self.markers[k] for k in self.markers if s.find(k) == s.rfind(k)}
        print("filter finished")
    def get_markers(self):
        return self.markers

    def write_as_json(self, path='.\\词库\\markers.json'):
        with open(path, 'w', encoding='u8') as markers_json_file:
            json.dump(self.markers, markers_json_file)
