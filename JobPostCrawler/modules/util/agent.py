#!/usr/bin/env python
# -*- coding:utf-8 -*-

import fake_useragent
import logging
import requests_html
import traceback

import config


__all__ = ["RequestFactory"]


class BaseRequest(object):

    def __init__(self, url):
        self.base_url = url  # Website main page
        self.request_url = ""  # Interface of the website
        self.session = requests_html.HTMLSession()
        self.__user_agent = fake_useragent.UserAgent()

        # self.__proxy_agent = proxy.FakeProxy()

    def request(self):
        """
        Send request to the website and get the response

        :return:
        """

        # Connect main page link with interface link
        url = self.base_url + self.request_url

        headers = {
            "Referer": url,
            "User-Agent": self.__user_agent.random
        }

        response = None

        timeout = 0  # Timeout counter

        # Timeout if it cannot acquire the response after requesting 5 times
        while not response:
            try:
                # proxies = self.__proxy_agent.get_proxy()

                response = self.session.get(url, headers=headers)
            except Exception as error:
                logging.error(error, exc_info=True)

                timeout += 1
                assert timeout <= 20, "Timeout"
            else:
                break

        log = "Response acquired"

        logging.info(log)

        return response

    def close(self):
        if self.session:
            self.session.close()
            self.session = None


class IndeedRequest(BaseRequest):

    __params_type = {
        "keyword": "q=",
        "location": "&l=",
    }

    def __init__(self, params):
        super(IndeedRequest, self).__init__(config.website_urls["indeed"])

        self.__params = params

    def set_search_parameter(self, next_page):
        self.request_url = "/jobs?"

        for i, key in enumerate(self.__params.keys()):
            if self.__params[key]:
                self.request_url += f"{self.__params_type[key]}{self.__params[key]}"

        if next_page > 0:
            self.request_url += f"&start={next_page}0"


class JobBankRequest(BaseRequest):

    pass


class RequestFactory(object):

    __request_type = {
        "indeed": IndeedRequest,
        "jobbank": JobBankRequest,
    }

    @classmethod
    def get_request(cls, option):
        return cls.__request_type[option]
