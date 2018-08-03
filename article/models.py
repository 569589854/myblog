# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:28:51
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-23 13:26:31
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid
from frontauth.models import FrontUserModel

class ArticleModel(models.Model):
    # 一个field传了editable=False 调用django 的 model_to_dict 将丢失该字段
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=True)
    author = models.ForeignKey(User,null=True)
    title = models.CharField(max_length=20)
    category = models.ForeignKey('CategoryModel')
    desc = models.CharField(max_length=100)
    thumbnail = models.URLField(max_length=100,blank=True)
    tags = models.ManyToManyField('TagModel')
    content_html = models.TextField(null=True)
    # auto_now_add : 第一次添加才更新时间
    # auto_now : .save() 自动更新当前时间
    public_date = models.DateTimeField(auto_now=True,null=True)
    update_date = models.DateTimeField(auto_now=True,null=True)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    top = models.ForeignKey('TopModel',null=True,on_delete=models.SET_NULL)

class TopModel(models.Model):
    Alter_time = models.DateTimeField(auto_now=True)

class CategoryModel(models.Model):
    name = models.CharField(max_length=20,unique=True)

class TagModel(models.Model):
    name = models.CharField(max_length=20,unique=True) 

class CommentModel(models.Model):
    author = models.ForeignKey(FrontUserModel)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(ArticleModel)
