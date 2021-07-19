#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
from os import path
from fake_useragent import UserAgent
import re


# default: not running as a .exe file
FROZEN = False
LOCAL = False

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    FROZEN = True
    MAIN_FILE = sys.argv[0]
    DIST_DIR = path.abspath(path.dirname(MAIN_FILE))

    if not path.exists(path.abspath(path.join(DIST_DIR, r"appdata"))):
        # appdata folder doesn't exists in the local machine
        bundle_dir = getattr(sys, "_MEIPASS", path.abspath(path.dirname(path.dirname(__file__))))
        APPDATA = path.abspath(path.join(bundle_dir, r"appdata"))
    else:
        # appdata folder exists in the local machine
        APPDATA = path.abspath(path.join(DIST_DIR, r"appdata"))
else:
    APPDATA = path.abspath(path.join(path.dirname(path.dirname(__file__)), r"appdata"))

DATABASE = path.abspath(path.join(APPDATA, r"database\report_url.mdb"))
REPORT_DIR = path.abspath(path.join(APPDATA, r"report\{}.pdf"))
PATTERN_LIB = path.abspath(path.join(APPDATA, r"pattern_lib.json"))

BASE_URL = r"http://stockdata.stock.hexun.com{}"
INIT_REQUEST = BASE_URL.format(r"/2009_ggqw_{}.shtml")

ADOCONNECTION = r"ADODB.Connection"
ADODBCOMMAND = r"ADODB.Command"
DSN = r"PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE={};".format(DATABASE)

CN_NUM = {"零": "0", "〇": "0", "一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8",
          "九": "9", "0": "0", 0: "0"}
TITLE_PATTERN = r"：([零〇一二三四五六七八九]|\d){{{}}}年({}|{}|{}|{})报告(?:（?全文）?|（?更新后）?)?$"

USERAGENT = UserAgent().random
