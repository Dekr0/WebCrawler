#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import sys
from os import path

sys.path.append(path.abspath(path.join(path.dirname(path.dirname(__name__)), "config")))
from .ado_util import ADOUtil
from .gui import show


class ReportQuery(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(ReportQuery, "_instance"):
            ReportQuery._instance = object.__new__(cls)
        return ReportQuery._instance

    def __init__(self):
        self.__handle()

    def __handle(self):
        show()
