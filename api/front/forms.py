# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:28:12
# @Last Modified by:   56958
# @Last Modified time: 2017-02-26 20:23:12
from django import forms
from api.common.forms import BaseForm
from django.core.cache import cache
from utils.captcha.xtcaptcha import Captcha

class CaptchaForm(forms.Form):
    captcha = forms.CharField(max_length=4,min_length=4,error_messages={"required": "验证码不能为空！"})
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        if not Captcha.check_captcha(captcha):
            raise forms.ValidationError(u'验证码错误！')

        return captcha    
class SignupForm(BaseForm,CaptchaForm):
    email = forms.EmailField(error_messages={"required": "请输入邮箱"})
    username = forms.CharField(max_length=20,min_length=4,error_messages={"required": "用户名不能为空！"})
    password = forms.CharField(max_length=20,min_length=6,error_messages={"required": "密码不能为空！"})
    captcha = forms.CharField(max_length=4,min_length=4)


class UpdateFrontProfileForm(BaseForm):
    front_username = forms.CharField(max_length=10,min_length=4)
    portrait = forms.URLField(max_length=100,required=False)
    email = forms.EmailField()

class SigninForm(BaseForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=20,min_length=6)
    remember = forms.BooleanField(required=False)

class ForgetpwdForm(BaseForm,CaptchaForm):
    email = forms.EmailField()

class ResetpwdForm(BaseForm):
    password = forms.CharField(max_length=20,min_length=6)
    password_repeat = forms.CharField(max_length=20,min_length=6)

    def clean(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError(u'两次输入密码不一致！')

        return self.cleaned_data

class CommentForm(BaseForm):
    content = forms.CharField(max_length=200)
    article_id = forms.CharField()