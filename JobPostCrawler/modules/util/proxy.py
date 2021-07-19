import bs4
import fake_useragent
import logging
import re
import requests
import time


__all__ = ["FakeProxy"]

_QUIT = "Check EventLog.log"


class FakeProxy:

    def __init__(self):
        self.__clock = time.time()
        self.__proxy_pool = []
        self.__response = None
        self.__user_agent = fake_useragent.UserAgent()

        self.update_proxy_pool()

    def get_proxy(self):
        """
        :return: Dictionary mapping protocol the URL of the proxy
        """

        # Update the proxy pool if the pool is empty or proxy pool is out of date
        # for 5 minutes
        if len(self.__proxy_pool) == 0 or self.__clock - time.time() >= 300:
            self.update_proxy_pool()

        proxy = self.__proxy_pool.pop()

        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}",
        }

        return proxies

    def __request(self):
        """

        :return:
        """
        url = "https://free-proxy-list.net/"

        headers = {
            "Referer": url,
            "User-Agent": self.__user_agent.random
        }

        self.__response = None
        timeout = 0

        while not self.__response:
            try:
                self.__response = requests.get(url, headers=headers)
            except Exception as error:
                logging.error(error)

                timeout += 1
                assert timeout <= 5, "Timeout"

    def update_proxy_pool(self):
        self.__request()

        html = self.__response.text
        soup = bs4.BeautifulSoup(html, "lxml")

        textarea = soup.find("textarea")
        content = textarea.text

        try:
            proxies = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}",
                                 content)

            assert len(proxies) > 0, "Failed to find any proxy"
        except AssertionError as error:
            print(error)
            logging.error(error)

            quit(_QUIT)
        else:
            self.__proxy_pool = proxies
            log = "proxy pool is up to date"

            print(log)
            logging.info(log)
