import json

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from restframework import models
from restframework.utils.permission import MyPermission
from rest_framework.throttling import BaseThrottle
from rest_framework.versioning import BaseVersioning
from restframework.utils.version import MyVersion
from rest_framework import serializers

# Create your views here.
ORDER_DICT = {
    1: {
        'name': '张三',
        'age': 20,
    },
    2: {
        'name': '李四',
        'age': 21,
    }
}


def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'msg': None,
        }
        try:
            username = request._request.POST.get('username')
            password = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=username, password=password).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            token = md5(username)
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)


# class MySerializer(serializers.Serializer):
# username = serializers.CharField()
# user_type = serializers.CharField(source="get_user_type_display")
# password = serializers.CharField()

# aa = serializers.SerializerMethodField() # 自定义序列化
#
# def get_aa(self, row):
#     userinfo_obj_list = row.all()
#     ret = []
#     for item in userinfo_obj_list:
#         ret.append({'username': item.username, 'password': item.password})
#     return ret


class MySerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source="get_user_type_display")

    # url= serializers.HyperlinkedIdentityField(view_name='OrderView', lookup_field='username')

    # aa = serializers.SerializerMethodField() # 自定义序列化
    #
    # def get_aa(self, row):
    #     userinfo_obj_list = row.all()
    #     ret = []
    #     for item in userinfo_obj_list:
    #         ret.append({'username': item.username, 'password': item.password})
    #     return ret

    class Meta:
        model = models.UserInfo
        # fields = '__all__' #自动生成全部字段
        fields = ['username', 'password', 'user_type', ]  # 自定义需要的字段
        depth = 1  # 1~10 展开深度
        extra_kwargs = {
            'url': {'view_name': 'OrderView', 'lookup_field': 'username'},
            'users': {'lookup_field': 'username'}
        }


class OrderView(APIView):
    # permission_classes = [MyPermission, ] 权限
    # versioning_class = MyVersion 版本
    # authentication_classes = [] 认证
    # throttle_classes = [] 节流
    # parser_classes = [] 解析器，解析前段返回的数据格式 JSONParser，FormParser，等等    request.data 取数据

    def get(self, request, username, *args, **kwargs):
        # self.dispatch()
        ret = {
            'code': 1000,
            'msg': '未被处理',
            'data': None,
        }
        userinfo_obj = models.UserInfo.objects.filter(username=username)
        # userinfo_obj = models.UserInfo.objects.all()
        userinfo = MySerializer(instance=userinfo_obj, many=True, context={'request': request})
        try:
            ret['data'] = userinfo.data
            ret['msg'] = '查询成功'
            ret['code'] = 1001

        except Exception as e:
            ret['msg'] = e
            ret['code'] = 1002
            print(e)
        print(ret)
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        # print(type(request._request))
        userinfo = models.UserInfo.objects.all()
        serializer = MySerializer(instance=userinfo, many=True)
        # print(serializer.data)
        ret = json.dumps(serializer.data, ensure_ascii=False)
        # print(ret)
        return HttpResponse(ret)
