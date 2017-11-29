import threading
import multiprocessing
import logging
import logging.handlers


class Listener(multiprocessing.Process):
    def __init__(self, record_queue):
        super().__init__()
        self.record_queue = record_queue

    def run(self):
        self.emit_record()

    def emit_record(self):
        Listener.configure()
        while True:
            record = self.record_queue.get()
            if record is None:
                break
            logging.getLogger().handle(record)

    @staticmethod
    def configure():
        h = logging.handlers.RotatingFileHandler(filename='crawl.log',mode='a', encoding='u8',
                                                 maxBytes=10*1024*1024, backupCount=5)
        c = logging.StreamHandler()
        f = logging.Formatter("%(asctime)s - %(processName)s - %(levelname)s - %(message)s",
                              datefmt="%y-%m-%d %H:%M:%S")
        h.setFormatter(f)
        c.setFormatter(f)

        root = logging.getLogger()
        root.addHandler(h)
        root.addHandler(c)
        root.setLevel(logging.INFO)
