#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import random
import re
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__name__)), "config")))
from .ado_util import *
from config.config import USERAGENT, REPORT_DIR
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


_REPORT_DIR = REPORT_DIR


def __open_pdf(title):
    path = _REPORT_DIR.format(title)
    if not os.path.exists(path):
        raise

    os.startfile(path)


_OPEN_PDF = __open_pdf


def show():
    app = QApplication(sys.argv)
    framework = MainFramework()
    logging.info("Widget are formed")
    window = QueryWindow(framework)

    logging.info("Show Query Window")
    window.show()

    logging.info("Query Window closed. Script finished")
    sys.exit(app.exec_())


class QueryWindow(QMainWindow):

    def __init__(self, widgets):
        super(QueryWindow, self).__init__()

        self.setWindowTitle("报告查询")
        self.resize(250, 100)

        self.setCentralWidget(widgets)


class SelectionWindow(QMainWindow):

    def __new__(cls, *args, **kwargs):
        if not hasattr(SelectionWindow, "_instance"):
            SelectionWindow._instance = QWidget.__new__(cls)
        return SelectionWindow._instance

    def __init__(self, widgets):
        super(SelectionWindow, self).__init__()
        self.widgets = widgets
        self.setWindowTitle("选择指定报告")

        self.widgets.confirm.clicked.connect(self.get_selection)

        self.setCentralWidget(self.widgets)

    @pyqtSlot()
    def get_selection(self):
        title = self.widgets.list_view.currentIndex().data()
        self.close()
        _OPEN_PDF(title)


class MainFramework(QWidget):

    def __init__(self):
        super(MainFramework, self).__init__()

        self.__util = ADOUtil()
        self.__conn = self.__util.conn
        self.__report_type = self.__util.get_report_type()

        self.sub_framework = None
        self.selection_window = None

        self.__init_completer()
        self.__init_stock_input()
        self.__init_year_input()
        self.__init_type_selection()

        self.button = QPushButton("查询")
        self.layout = QVBoxLayout()

        self.button.clicked.connect(self.query)

        self.layout.addWidget(self.stock_box)
        self.layout.addWidget(self.year_box)
        self.layout.addWidget(self.type_box)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def __add_stock(self, iterable):
        self.model.setStringList(iterable)

    def __get_url(self, sql, total):
        count = 1
        (rs, result) = self.__conn.Execute(sql)
        url_dict = dict()

        flag = False
        if total > 1:
            flag = True

        while not rs.EOF:
            code = rs.Fields("股票代码").Value
            name = rs.Fields("股票名称").Value
            year = int(rs.Fields("年度").Value)
            rtype_code = int(rs.Fields("报告编号").Value)
            rtype = list(self.__report_type.keys())[list(self.__report_type.values()).index(rtype_code)]
            url = rs.Fields("网址").Value

            if not flag:
                report_title = "{}-{}{}{}报告".format(code, name, year, rtype)
            else:
                report_title = "{}-{}{}{}报告({})".format(code, name, year, rtype, count)
                count += 1

            url_dict[report_title] = url
            rs.MoveNext()

        rs.Close()

        return url_dict

    def __init_completer(self):
        self.completer = QCompleter()
        self.model = QStringListModel()

        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setModel(self.model)

        self.completer.activated.connect(self.unblock)
        self.completer.highlighted.connect(self.block)

    def __init_stock_input(self):
        self.stock_box = QGroupBox("股票代码和股票名称")
        self.stock_layout = QHBoxLayout()
        self.stock_input = QLineEdit()

        self.stock_input.setCompleter(self.completer)
        self.stock_input.textChanged.connect(self.search_factor)

        self.stock_layout.addWidget(self.stock_input)

        self.stock_box.setLayout(self.stock_layout)

    def __init_year_input(self):
        self.year_box = QGroupBox("年度")
        self.year_layout = QHBoxLayout()
        self.year_input = QLineEdit()

        self.year_input.setValidator(QRegExpValidator(QRegExp("\d{0,4}")))

        self.year_layout.addWidget(self.year_input)

        self.year_box.setLayout(self.year_layout)

    def __init_type_selection(self):
        self.type_box = QGroupBox("报告类型")
        self.type_layout = QHBoxLayout()
        self.type_combobox = QComboBox()

        self.type_combobox.addItems(self.__report_type.keys())

        self.type_layout.addWidget(self.type_combobox)

        self.type_box.setLayout(self.type_layout)

    def __show_selection_window(self, title_list):
        self.sub_framework = SubFramework()
        self.sub_framework.model.setStringList(title_list)
        self.selection_window = SelectionWindow(self.sub_framework)
        self.selection_window.show()

    @pyqtSlot()
    def block(self):
        if not self.stock_input.signalsBlocked():
            self.stock_input.blockSignals(True)

    @pyqtSlot()
    def unblock(self):
        if self.stock_input.signalsBlocked():
            self.stock_input.blockSignals(False)
            self.model.setStringList([])

    @pyqtSlot()
    def search_factor(self):
        text = self.stock_input.text().strip()
        if text:
            if re.fullmatch("\d{1,6}", text):
                self.__add_stock(self.__util.default_search("股票代码", text))
            elif re.fullmatch("[a-zA-Z ]+", text):
                self.pinyin_search(text)
            else:
                self.__add_stock(self.__util.default_search("股票名称", text))

    @pyqtSlot()
    def query(self):
        stock = self.stock_input.text().strip()
        year = self.year_input.text().strip()
        try:
            (code, name) = stock.split("-")
            report_type = self.__report_type[self.type_combobox.currentText()]

            query = r"SELECT * FROM PDF网址 WHERE 股票代码='{}'AND 股票名称='{}' AND 年度={} AND 报告编号={}" \
                .format(code, name, int(year), report_type)
            cquery = r"SELECT COUNT(*) AS 数量 FROM ({})".format(query)
            (com, result) = self.__conn.Execute(cquery)
            count = com.Fields("数量").Value
            com.Close()

            if not count:
                raise

            url_dict = self.__get_url(query, count)
            self.report_manage(url_dict, count)

        except Exception as ex:
            logging.critical(ex)
            QMessageBox.about(self, "查询错误", "查询结果不存在")

    def download_reports(self, title, url):
        header = {
            "user-agent": USERAGENT,
            "referrer": url
        }
        try:
            path = _REPORT_DIR.format(title)
            if not os.path.exists(path):
                logging.info("Try to download report from {} to local".format(url))
                with requests.get(url, headers=header) as res:
                    with open(path, "wb") as file:
                        for chunk in res.iter_content(1024):
                            file.write(chunk)
        except Exception as ex:
            logging.critical(ex)
            QMessageBox.about(self, "下载错误", "无法下载或在本地写入指定报告")

    def pinyin_search(self, string):
        pass

    def report_manage(self, url_dict, total):
        for title, url in url_dict.items():
            self.download_reports(title, url)
        try:
            if total > 1:
                logging.info("Show Selection Window")
                self.__show_selection_window(list(url_dict.keys()))
                logging.info("Show Selection Window Close")
            else:
                _OPEN_PDF(list(url_dict.keys())[0])
        except Exception as ex:
            logging.critical(ex)
            QMessageBox.about(self, "本地错误", "无法打开本地的报告")


class SubFramework(QWidget):

    def __new__(cls, *args, **kwargs):
        if not hasattr(SubFramework, "_instance"):
            SubFramework._instance = QWidget.__new__(cls)
        return SubFramework._instance

    def __init__(self):
        super(SubFramework, self).__init__()

        self.layout = QVBoxLayout()
        self.label = QLabel("出现多份拥有相同报告信息但不同网址的报告, 请选择需要查看的报告")
        self.confirm = QPushButton("确认")
        self.model = QStringListModel()
        self.list_view = QListView()
        self.button_box = QHBoxLayout()

        self.list_view.setModel(self.model)

        self.button_box.addWidget(self.confirm)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.list_view)
        self.layout.addLayout(self.button_box)

        self.setLayout(self.layout)
