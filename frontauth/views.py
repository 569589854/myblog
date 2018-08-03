# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:29:26
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 20:59:16
from django.shortcuts import render
from django.http import HttpResponse
from models import FrontUserModel
from utils import login,logout
import configs
from decorators import front_login_required

def add_user(request):
    user = FrontUserModel(email='ccc@qq.com',username='Leo',password='123')
    user.save()
    return HttpResponse('success')

def test1(request):
    # 数据库中查找用户 验证密码是否匹配
    email = 'ccc@qq.com'
    password = '123'
    user = FrontUserModel.objects.filter(email=email).first()
    user.update_password('456')
    # if user.check_password(password):
    #     return HttpResponse('验证成功！')
    # else:
    #     return HttpResponse('验证失败！')
    return HttpResponse('密码更改成功！')

def front_login(request):
    email = 'ccc@qq.com'
    password = '456'

    user = login(request,email,password)
    if user:
        return HttpResponse(u'登录成功！')
    else:
        return HttpResponse(u'登录失败！')

def check_login(request):
    uid = request.session.get(configs.LOGINED_KEY)
    user = FrontUserModel.objects.filter(pk=uid).first()
    if user:
        return HttpResponse('验证成功！')
    else:
        return HttpResponse('验证失败！')

def front_logout(request):
    logout(request)
    return HttpResponse(u'退出成功！')

@front_login_required
def decorator_check(request):
    return HttpResponse(u'你已登录！')

def middleware_test(request):
    if hasattr(request,'front_user'):
        return HttpResponse('failed')
    else:
        return HttpResponse('success')