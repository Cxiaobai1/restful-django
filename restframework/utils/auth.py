# -*- coding: utf-8 -*-
# @Time    : 2021/11/20 13:26
# @Author  : Cxiaobai
# @Email   : 494158341@qq.com
# @File    : auth.py
# @Software: PyCharm
from restframework import models
from rest_framework.request import exceptions
from rest_framework.authentication import BaseAuthentication, BasicAuthentication


class Authtication(BaseAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get('token')
        # print(token)
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return token_obj.user, token_obj

    def authenticate_header(self, request):
        pass


class Token(BasicAuthentication):
    model = models.UserToken
