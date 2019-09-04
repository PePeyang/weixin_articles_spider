import threading
import Queue

from twisted.internet import reactor

from scrapy.xlib.pydispatch import dispatcher
from scrapy.core.manager import scrapymanager
from scrapy.core.engine import scrapyengine
from scrapy.core import signals


class CrawlerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False

    def run(self):
        self.running = True
        scrapymanager.configure(control_reactor=False)
        scrapymanager.start()
        reactor.run(installSignalHandlers=False)

    def crawl(self, *args):
        if not self.running:
            raise RuntimeError("CrawlerThread not running")
        self._call_and_block_until_signal(signals.spider_closed,
                                          scrapymanager.crawl, *args)

    def stop(self):
        reactor.callFromThread(scrapyengine.stop)

    def _call_and_block_until_signal(self, signal, f, *a, **kw):
        q = Queue.Queue()

        def unblock():
            q.put(None)
        dispatcher.connect(unblock, signal=signal)
        reactor.callFromThread(f, *a, **kw)
        q.get()
