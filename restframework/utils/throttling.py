# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 16:36
# @Author  : Cxiaobai
# @Email   : 494158341@qq.com
# @File    : throttling.py
# @Software: PyCharm

from rest_framework.throttling import SimpleRateThrottle


class MyThrottling(SimpleRateThrottle):
    scope = 'll'

    def get_cache_key(self, request, view):
        return self.get_ident(request)
