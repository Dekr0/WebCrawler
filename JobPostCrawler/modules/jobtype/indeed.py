#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime


class IndeedJob:

    def __init__(self, company, day_post, id, link, location, summary, title):
        self.company = company
        self.day_post = day_post
        self.id = id
        self.link = link
        self.location = location
        self.summary = summary
        self.title = title
        self.update_time = str(datetime.datetime.now())

    @staticmethod
    def get_columns_def():
        """
        :return: a dictionary that specify the data type and length in SQL for each
        column
        """

        columns_def = {
            "Id": "VARCHAR(32)",
            "Title": "VARCHAR(MAX)",
            "Location": "VARCHAR(60)",
            "Company": "VARCHAR(180)",
            "DayPost": "VARCHAR(30)",
            "Summary": "VARCHAR(MAX)",
            "Link": "VARCHAR(MAX)",
            "UpdateTime": "VARCHAR(120)",
         }

        return columns_def

    def get_info(self):
        """
        :return: job information
        """

        info = {
            "Id": self.id,
            "Title": self.title,
            "Location": self.location,
            "Company": self.company,
            "DayPost": self.day_post,
            "Summary": self.summary,
            "Link": self.link,
            "UpdateTime": self.update_time,
        }

        return info
