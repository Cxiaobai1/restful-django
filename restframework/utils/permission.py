# -*- coding: utf-8 -*-
# @Time    : 2021/11/20 15:34
# @Author  : Cxiaobai
# @Email   : 494158341@qq.com
# @File    : permission.py
# @Software: PyCharm
from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    # message = '1'

    def has_permission(self, request, view):
        if request.user.user_type == 1:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True
