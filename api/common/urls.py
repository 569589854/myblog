# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-02 09:14:46
# @Last Modified by:   Mack
# @Last Modified time: 2016-11-02 10:15:40
from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^captcha/',views.captcha,name='common_captcha'),
]