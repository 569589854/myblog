# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-23 16:09:23
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-13 20:11:54
from django.http import HttpResponse,JsonResponse
from collections import namedtuple

"""
http状态码:
200: 请求正常(ok)
400: 请求参数错误(paramserror)
401: 没有权限访问(unauth)
405: 请求方法错误(methoderror)
""" 

HttpCode = namedtuple('HttpCode',['ok','paramserror','unauth','methoderror'])
httpCode = HttpCode(ok=200,paramserror=400,unauth=401,methoderror=405)

# 请求正常的json返回函数
def json_result(code=httpCode.ok,message='',data={},kwargs={}):
    json = {'code':code,'message':message,'data':data}
    # 把json和kwargs合并成一个字典
    if kwargs.keys():
        # json = dict(json,**kwargs)
        for k,v in kwargs.items():
            json[k] = v
    return JsonResponse(json)

def json_params_error(message=''):
    """
        请求参数错误
    """
    return json_result(code=httpCode.paramserror,message=message)

def json_unauth_error(message=''):
    """
        没有权限访问
    """
    return json_result(code=httpCode.unauth,message=message)

def json_method_error(message=''):
    """
        请求方法错误
    """
    return json_result(code=httpCode.methoderror,message=message)

