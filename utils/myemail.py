# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2017-01-22 22:00:32
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-23 14:59:56
import hashlib
from django.core.cache import cache
from django.shortcuts import reverse
from django.conf import settings
import time
from django.core import mail

def send_email(request,email,check_url,subject=None,cache_data=None,message=None,signup=None):
    # 发送链接到email这个邮箱,用户点击才算验证成功
    code = hashlib.md5(str(time.time())+email).hexdigest()
    # 1.邮箱信息保存到缓存中
    # 2.发送邮件到email这个邮箱
    if cache_data:
        cache.set(code,cache_data,600)
    else:    
        cache.set(code,email,600)
    if not subject:
        subject = u"邮箱修改验证"
    url = reverse(check_url,kwargs={'code':code})      #获取url
    scheme = request.scheme + '://'                            #获取协议
    host = request.get_host()                                  #获取域名
    check_URL = scheme + host + url
    if not message:
        message = u' 完成博客邮箱验证,请在10分钟内完成验证，工作人员不会向您索取验证码，请勿泄露。消息来自：Mack的博客'
    # link_url中应该包含验证链接
    if not signup:
        link_url = u'点击链接 ' + check_URL + message
    else:
        link_url = u'恭喜！您已注册成功！点击链接 ' + check_URL + message
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    # print 'url:',check_URL
    if mail.send_mail(subject,link_url,from_email,recipient_list):
        return True
    else:
        return False