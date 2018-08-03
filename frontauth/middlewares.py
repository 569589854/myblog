# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2017-01-22 20:41:44
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 21:17:32
from django.utils.deprecation import MiddlewareMixin
from models import FrontUserModel
import configs

class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
 
        # 1.若用户已登录 则添加front_user属性
        if request.session.get(configs.LOGINED_KEY):
            # 2.判断当前request是否已添加front_user属性,避免重复添加
            if not hasattr(request,'front_user'):
                uid = request.session.get(configs.LOGINED_KEY)
                # 若无.first() 则user为一个QuerySet
                user = FrontUserModel.objects.filter(pk=uid).first()
                setattr(request,'front_user',user) 