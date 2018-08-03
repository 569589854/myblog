# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2017-01-22 21:48:26
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 21:48:59
from django import forms
import json
from utils import myjson

class BaseForm(forms.Form):
    def get_error(self):
        # 将错误信息以json形式显示
        errors = self.errors.as_json()  # str类型
        # 转换成字典
        error_dict = json.loads(errors) # dict类型
        message = '' # 若message为空则返回空
        # 只取字典中第一个值
        # {u'captcha': [{u'message': u'\u9a8c\u8bc1\u7801\u9519\u8bef',}]}
        for k,v in error_dict.items():  # v0 为数组message的value
            message = v[0].get('message',None)
        print type(error_dict)
        return message

    # 封装获取错误信息函数
    def get_error_response(self):
        if self.errors:
            return myjson.json_params_error(message=self.get_error())
        else:
            return myjson.json_result()
