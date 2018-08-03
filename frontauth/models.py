# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:29:26
# @Last Modified by:   56958
# @Last Modified time: 2017-02-26 10:53:37
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid
import hashlib
import hashers

class FrontUserModel(models.Model):
    # 用户相关的表 不要使用自增长的id做主键
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    portrait = models.URLField(blank=True)
    # 拉黑用户 封号
    is_active = models.BooleanField(default=True)
    # 用户申请时间
    dete_joined = models.DateTimeField(auto_now_add=True)
    # 用户最后一次登陆
    last_login = models.DateTimeField(null=True,blank=True)

    def __init__(self,*args,**kwargs):
        if 'password' in kwargs:
            hash_password = hashers.make_password(kwargs['password'])
            kwargs['password'] = hash_password
        super(FrontUserModel,self).__init__(*args,**kwargs)


    # 验证密码
    def check_password(self,raw_password):
        return hashers.check_password(raw_password,self.password)
        #这里的self.password 即数据库中已被加密的密码


    # 更新密码
    def update_password(self,raw_password):
        # # 若不满足条件 直接抛出异常
        # assert raw_password
        if not raw_password:
            return None

        hash_password = hashers.make_password(raw_password)
        self.password = hash_password
        self.save(update_fields=['password'])

class FrontUser(models.Model):
    portrait = models.URLField(max_length=100,blank=True)
    # 使用一对一，django中的User模型必须和FrontUser中的一一对应
    # 不能出现一个User对应多个FrontUser的情况
    # 外键使用在一对多上
    user = models.OneToOneField(FrontUserModel)
