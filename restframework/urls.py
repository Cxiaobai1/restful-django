# -*- coding: utf-8 -*-
# @Time    : 2021/11/19 13:54
# @Author  : Cxiaobai
# @Email   : 494158341@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path
from restframework import views

app_name = 'restframework'
urlpatterns = [
    path('auth/', views.AuthView.as_view(), name='AuthView'),
    path('order/<str:username>/', views.OrderView.as_view(), name='OrderView'),
]
