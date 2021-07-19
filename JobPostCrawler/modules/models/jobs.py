#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime

import modules.models.structure as structure


class IndeedJobsSet:

    def __init__(self):
        self.__jobs_list = []
        self.__index = 0

    def __len__(self):
        return len(self.__jobs_list)

    def __iter__(self):
        return iter(self.__jobs_list)

    def add_job(self, job):
        self.__jobs_list.append(job)


class IndeedJobPosts(structure.IterableQueue):

    def __init__(self):
        super(IndeedJobPosts, self).__init__()


class IndeedJobs:

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
