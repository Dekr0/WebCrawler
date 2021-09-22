#!/usr/bin/env python
# -*- coding:utf-8 -*-


__all__ = ["URLEncoder"]


def _htmlEncoder(char):
    return "+" if char.isspace() else f"%{hex(ord(char)).split('x')[1].upper()}"


def URLEncoder(params):
    """
    Convert the special characters in the parameters string into the HTML encoder

    :param params: parameters for requesting a response
    :return:
    """

    for key in params.keys():
        params[key] = "".join([char if char.isdigit() or char.isalpha() else
                               _htmlEncoder(char) for char in params[key]])

    return params