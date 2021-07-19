#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

Provide method to access table and data in the database

"""

import sys
from win32com import client
from config.config import *
from config.ADOConstants import *

_ADOCONNECTION = ADOCONNECTION
_ADODBCOMMAND = ADODBCOMMAND
_DATABASE = DATABASE
_DSN = DSN


def _init_params(cmd, flag=0):
    params = dict()
    params["stock_id"] = cmd.CreateParameter("stock_id", adVarChar, adParamInput, 1024)
    params["stock_name"] = cmd.CreateParameter("stock_name", adVarChar, adParamInput,
                                               1024)
    params["year"] = cmd.CreateParameter("year", adInteger, adParamInput)
    params["report_type"] = cmd.CreateParameter("report_type", adInteger, adParamInput)
    if not flag:
        params["url"] = cmd.CreateParameter("url", adVarChar, adParamInput, 1024 * 4)
    params["year"].NumericScale = 0
    params["report_type"].NumericScale = 0

    for key in params.keys():
        cmd.Parameters.Append(params[key])

    return params


class ADOUtil(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(ADOUtil, "_instance"):
            ADOUtil._instance = object.__new__(cls)
        return ADOUtil._instance

    def __init__(self):
        self.__get_conn()

        self.check_url = self.__check_url
        self.default_search = self.__default_search
        self.get_report_type = self.__get_report_type
        self.get_insert_command = self.__get_insert_command
        self.get_latest_year = self.__get_latest_year
        self.get_stock_id = self.__get_stock_id
        self.get_url_list = self.__get_url_list

    def __get_conn(self):
        if not hasattr(self, "conn"):
            try:
                conn = client.Dispatch(_ADOCONNECTION)
                conn.Open(_DSN)
                if not conn.State == adStateOpen:
                    raise Exception

                self.conn = conn
            except Exception as ex:
                sys.exit("Failed to connect ot database: {}".format(ex))

    def __get_insert_command(self):
        """
        Create an modified ADO Command object with unfilled, customized parameters for insert data into the database.
        """

        if not hasattr(self, "insert_cmd") or not hasattr(self, "insert_params"):
            self.insert_cmd = client.Dispatch(_ADODBCOMMAND)
            self.insert_cmd.ActiveConnection = self.conn  # Attach to an ADO Connection object instance
            self.insert_cmd.CommandType = adCmdText  # Type of command being used

            # "?" servers as a placeholder for a customized parameter
            query = r"INSERT INTO PDF网址(股票代码, 股票名称, 年度, 报告编号, 网址) VALUES (?, ?, ?, ?, ?)"
            self.insert_cmd.CommandText = query
            self.insert_params = _init_params(self.insert_cmd)

        return self.insert_cmd, self.insert_params

    def __check_url(self, url):

        query = "SELECT 1 FROM PDF网址 WHERE 网址='{}'".format(url)
        (rs, result) = self.conn.Execute(query)
        if not rs.BOF and not rs.EOF:
            return True
        return False

    def __default_search(self, flag, string):

        query = r"SELECT * FROM 股票代码 WHERE {} LIKE '%{}%'".format(flag, string)
        stock_list = []

        (rs, result) = self.conn.Execute(query)
        while not rs.EOF:
            code = rs.Fields("股票代码").Value
            name = rs.Fields("股票名称").Value
            stock_list.append("{}-{}".format(code, name))
            rs.MoveNext()

        rs.Close()

        return stock_list

    def __get_latest_year(self):
        if not hasattr(self, "latest_year"):
            query = "SELECT MAX(年度) AS latest_year FROM PDF网址"
            (rs, result) = self.conn.Execute(query)
            self.latest_year = int(rs.Fields("latest_year").Value) if rs.Fields("latest_year").Value else 2010
            rs.Close()

        return self.latest_year

    def __get_stock_id(self):
        if not hasattr(self, "stock_id"):
            self.stock_id = dict()
            query = "SELECT 股票代码, 股票名称 FROM 股票代码"
            (rs, result) = self.conn.Execute(query)

            while not rs.EOF:
                self.stock_id[rs.Fields("股票代码").Value] = rs.Fields("股票名称").Value
                rs.MoveNext()
            rs.Close()

        return self.stock_id

    def __get_report_type(self):
        if not hasattr(self, "report_type"):
            self.report_type = dict()
            query = "SELECT * FROM 报告类型"
            (rs, result) = self.conn.Execute(query)

            while not rs.EOF:
                self.report_type[rs.Fields("报告类型").Value] = int(rs.Fields("报告编码").Value)
                rs.MoveNext()
            rs.Close()

        return self.report_type

    def __get_url_list(self):
        if not hasattr(self, "url_list"):
            query = "SELECT * FROM PDF网址"
            (rs, result) = self.conn.Execute(query)
            self.url_list = []

            while not rs.EOF:
                url = rs.Fields("网址").Value
                self.url_list.append(url)
                rs.MoveNext()

        return self.url_list
