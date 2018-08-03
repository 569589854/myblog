# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-02 09:14:52
# @Last Modified by:   Mack
# @Last Modified time: 2016-11-02 20:56:27
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from utils.captcha.xtcaptcha import Captcha
from django.core.cache import cache
from PIL import Image
try:
    from cStringIO import cStringIO
except ImportError:
    from io import BytesIO as StringIO 

def captcha(request):
    text,image = Captcha.gene_code()
    # 将图片保存到本地
    # image.save('text.png','png')
    # 需要通过StringIO这个类来把图片当成流的形式返回给客户端
    out = StringIO() # 获取管道
    # 将图片保存到管道
    image.save(out,'png')
    # 移动文件指针到第0位置
    out.seek(0)
    # 指定返回的是image的png格式
    response = HttpResponse(content_type='image/png')
    # 从0位置开始读图片
    response.write(out.read())
    # 把验证码数据写入到缓存中,过期时间设置2分钟
    # key = text.lower()
    # value = key
    # cache.set(key,text,120) 
    return response