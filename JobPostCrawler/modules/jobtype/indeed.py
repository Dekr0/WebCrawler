#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime


class IndeedJob:

    def __init__(self, company, postedDay, id, link, location, summary, title):
        self.company = company
        self.postedDay = postedDay
        self.id = id
        self.link = link
        self.location = location
        self.summary = summary
        self.title = title
        self.updatedTime = str(datetime.datetime.now())

    @staticmethod
    def getColumnType():
        """
        :return: a dictionary that specify the data type and length in SQL for each
        column
        """

        columnType = {
            "Id": "VARCHAR(32)",
            "Title": "VARCHAR(MAX)",
            "Location": "VARCHAR(60)",
            "Company": "VARCHAR(180)",
            "PostedDay": "VARCHAR(30)",
            "Summary": "VARCHAR(MAX)",
            "Link": "VARCHAR(MAX)",
            "UpdatedTime": "VARCHAR(120)",
         }

        return columnType

    def getJobInfo(self):
        """
        :return: job information
        """

        info = {
            "Id": self.id,
            "Title": self.title,
            "Location": self.location,
            "Company": self.company,
            "PostedDay": self.postedDay,
            "Summary": self.summary,
            "Link": self.link,
            "UpdatedTime": self.updatedTime,
        }

        return info
