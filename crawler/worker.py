from threading import Thread
from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
import threading

class Worker(Thread):
    def __init__(self, worker_id, config, frontier, result):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.result = result
        self.shutdown_request = False
        self.shutdown_lock = threading.Lock()
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
                # f"Content length: {len(resp.raw_response.content) if resp.raw_response else 0} bytes.")
            scraped_urls = scraper.scraper(tbd_url, resp, self.result)
            # self.logger.info(
            #     f"Scraped {len(scraped_urls)} urls from {tbd_url}."
            #     f"Adding scraped urls to frontier."
            #     f"Result: {self.result.__dict__}"
            # )
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)

    def request_shutdown(self):
        with self.shutdown_lock:
            self.shutdown_request = True

    def check_shutdown_request(self):
        with self.shutdown_lock:
            return self.shutdown_request
        
    def graceful_shutdown(self):
        self.request_shutdown()
        self.join()
        self.logger.info(f"Worker-{self.ident} has shutdown gracefully.")
        return