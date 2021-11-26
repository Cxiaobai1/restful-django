# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 13:37
# @Author  : Cxiaobai
# @Email   : 494158341@qq.com
# @File    : version.py
# @Software: PyCharm
from rest_framework.versioning import BaseVersioning,QueryParameterVersioning,URLPathVersioning


class MyVersion(URLPathVersioning):
    pass
