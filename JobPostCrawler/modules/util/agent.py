#!/usr/bin/env python
# -*- coding:utf-8 -*-

import fake_useragent
import logging
import requests_html
import config


__all__ = ["RequestFactory"]


class WebsiteRequest(object):

    """
    A generic class for sending request to website. All the inherited class will
    use the same request() and close() methods.

    All the inherited class will implement their own set_search_parameter()
    methods to construct a formatted string, which includes the search parameters
    . The format of that string is varied depend on which website you want to
    search.
    """

    def __init__(self, url):
        """
        websiteUrl : Url to website main page

        searchParameters : A formatted string that include all the search
        parameter. The format depends on what website you want to search

        :param url: Url to website main page
        """

        self.websiteUrl = url
        self.searchParameters = ""
        self.session = requests_html.HTMLSession()
        self.__userAgent = fake_useragent.UserAgent()


    def request(self):
        """
        Send request to the website and get the response

        :return: A response instance. Usually it is the first page of the search
        result
        """

        requestUrl = self.websiteUrl + self.searchParameters

        headers = {
            "Referer": requestUrl,
            "User-Agent": self.__userAgent.random
        }

        response = None

        timeout = 0  # Timeout counter

        # Timeout if it cannot acquire the response after requesting 5 times
        while not response:
            try:
                response = self.session.get(requestUrl, headers=headers)
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


class IndeedRequest(WebsiteRequest):

    paramsType = {
        "keyword": "q=",
        "location": "&l=",
    }

    def __init__(self, params):
        super(IndeedRequest, self).__init__(config.websiteURLs["indeed"])

        self.__params = params

    def set_search_parameter(self, next_page):
        """
        Joint the search parameter and the URL of Indeed main page together.
        Use for sending request to Indeed

        :param next_page: ...
        :return:
        """

        self.searchParameters = "/jobs?"

        for i, key in enumerate(self.__params.keys()):
            if self.__params[key]:
                self.searchParameters += f"{self.paramsType[key]}{self.__params[key]}"

        if next_page > 0:
            # Correct the format of the page index in the search parameter. If
            # the current page is not the first page, it needs to append an
            # extra 0 at the end (greater than 9 : 100, 110, 120, etc.)
            self.searchParameters += f"&start={next_page}0"


class JobBankRequest(WebsiteRequest):

    pass


class RequestFactory(object):

    """
    This class is used for initialization of a website request based on what
    website you to search for.
    """

    __websiteRequest = {
        "indeed": IndeedRequest,
        "jobbank": JobBankRequest,
    }

    @classmethod
    def get_request(cls, option):
        return cls.__websiteRequest[option]
