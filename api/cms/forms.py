# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:27:16
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 21:48:13
from django import forms
from utils.captcha.xtcaptcha import Captcha
import json
from utils import myjson
from api.common.forms import BaseForm

class LoginForm(BaseForm):
    username = forms.CharField(max_length=10,min_length=4)
    password = forms.CharField(max_length=20,min_length=6)
    captcha = forms.CharField(max_length=4,min_length=4)
    remember = forms.CharField(required=False)#有可能不需要记住我

    def clean_captcha(self):
        # 获取验证码 name="captcha"
        captcha = self.cleaned_data.get('captcha',None)
        # 如果返回True 则返回验证码
        if not Captcha.check_captcha(captcha):
            raise forms.ValidationError(u'验证码错误!')
        else:
            return captcha

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


class UpdateProfileForm(BaseForm):
    username = forms.CharField(max_length=10,min_length=4)
    portrait = forms.URLField(max_length=100,required=False)

class UpdateEmailForm(BaseForm):
    email = forms.EmailField(required=True)

class AddCategoryForm(BaseForm):
    categoryname = forms.CharField(max_length=20)

class AddTagForm(BaseForm):
    tagname = forms.CharField(max_length=20)

class AddArticleForm(BaseForm):
    title = forms.CharField(max_length=200)    
    category = forms.IntegerField()
    desc = forms.CharField(max_length=100,required=False)
    thumbnail = forms.URLField(max_length=100,required=False)
    content_html = forms.CharField()

    #author,tags
    # tags是通过数组的形式上传 forms中没有合适的field进行验证
    # author不需要验证

class UpdateArticleForm(AddArticleForm):
    uid = forms.UUIDField()

class DeleteArticleForm(BaseForm):
    uid = forms.UUIDField(error_messages={'required':u'获取不到文章id!'})

class TopArticleForm(DeleteArticleForm):
    pass

class CategoryForm(BaseForm):
    category_id = forms.IntegerField()

class EditCategoryForm(CategoryForm):
    name = forms.CharField()