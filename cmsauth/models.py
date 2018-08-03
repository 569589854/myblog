# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-07 18:11:03
# @Last Modified by:   56958
# @Last Modified time: 2017-03-11 17:18:20
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CmsUser(models.Model):
    portrait = models.URLField(max_length=100,blank=True)
    # 使用一对一，django中的User模型必须和CmsUser中的一一对应
    # 不能出现一个User对应多个CmsUser的情况
    # 外键使用在一对多上
    user = models.OneToOneField(User)