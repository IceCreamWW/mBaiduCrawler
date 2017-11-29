import re
import os
import logging

from CrawlConfig import CrawlConfig
from multiprocessing import Process


class ContextDealer(Process, CrawlConfig):
    def __init__(self, file_lock, file_cnt, content_queue, mark, markers, record_queue):
        Process.__init__(self)
        CrawlConfig.__init__(self)
        self.markers = markers
        self.file_lock = file_lock
        self.record_queue = record_queue
        self.mark = mark
        self.file_cnt = file_cnt
        self.content_queue = content_queue
        self.url = ""

    def run(self):
        self.log_config(self.record_queue)
        self.deal()

    def deal(self):
        while True:
            content = self.content_queue.get()
            if content is None:
                return
            self.url = content[:content.index("$$$")]
            content = content[content.index("$$$") + 3:]

            content = self.content_filter(content)
            self.result_writer(content)

    def content_filter(self, content):
        # 删除所有HTML符号实体
        content = re.sub(r'&[\w]+', ' ', content, re.A)
        # 删除文本效果标签
        pattern = r'</*(' + '|'.join(self.TEXT_MARK) + ')( .*?>|>)'
        content = re.sub(pattern, '', content)
        # 删除注释
        content = re.sub(r'/\*.*?\*/', '\n', content)
        # 删除所有无文本意义标签
        pattern = r'<(' + '|'.join(self.DEL_MARK) + ').*?>[\s\S]*?</(' + '|'.join(self.DEL_MARK) + ')>'
        content = re.sub(pattern, '\n', content)
        # 删除所有其它标签
        content = re.sub(r'<.*?>', '\n', content)
        # 删除所有大量的连续英文
        content = re.sub(r'[\n\r ]{2,}', '\n', content)
        content = re.sub(r'[^\u4E00-\u9FA5（）【】，。？：“”‘’！《》*·]{30,}', '\n', content, flags=re.A)
        # 格式处理
        content = re.sub(r'^[\n \t]+', '', content)
        content = re.sub(r'[\n \t]+$', '', content)
        # 删除单行过短
        content = re.sub(r'(?<=\n)[^\n]{0,10}\n', '', content)
        # 开始文本标记 忽略大小写
        for keyword in self.markers:
            content = re.sub(
                '(?i)' + keyword, '[' + keyword + '][' + self.markers[keyword] + ']', content)
        return content

    def result_writer(self, content):
        if len(content) < 1000:
            logging.warning("Deleted : Too Short - " + self.url)
            return
        if len(re.findall('\[' + self.mark + '\d\]', content)) < self.min_marks:
            logging.warning("Deleted : Too Few Marks - " + self.url)
            return

        self.file_lock.acquire()
        f = open('.\\语料\\' + str(self.file_cnt.value) + '.txt', 'w', encoding='u8')
        self.file_cnt.value += 1
        logging.warning("Success : " + os.path.basename(f.name) + ' - ' + self.url)
        self.file_lock.release()

        f.write(content)
        f.close()
