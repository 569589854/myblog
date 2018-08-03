# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2017-01-22 19:32:36
# @Last Modified by:   56958
# @Last Modified time: 2017-02-25 14:34:45

# 实现 一个login_required的装饰器
"""
    需求：
    1.如果用户没有登录，跳转到登陆页面
    2.如果用户已经登录，不执行任何操作
    3.如果用户已经登录，跳转到登陆页面，且需要添加一个next的url到当前url中 
"""
from models import FrontUserModel
import configs
from django.shortcuts import redirect,reverse
from django.http import HttpResponse

def front_login_required(func):
    def wrapper(request,*args,**kwargs):
        uid = request.session.get(configs.LOGINED_KEY)
        if uid:
            # session中存在uid  说明已经登录
            return func(request,*args,**kwargs)
        else:
            # session中不存在uid  说明没有登录 跳转到登陆页面
            url = reverse('front_signin') + '?next=' + request.path # /auth/decorator_check
            # /cms/login/?next=/cms/
            return redirect(url)
    return wrapper 