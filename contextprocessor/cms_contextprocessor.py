# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-16 14:23:48
# @Last Modified by:   Mack
# @Last Modified time: 2016-11-16 14:37:48
from django.contrib.auth.models import User
from cmsauth.models import CmsUser

def CmsContextProcessor(request):
    user = request.user
    # 给user添加一个portrait属性
    # portrait属性存储在CmsUser里面
    # 把CmsUser的portrait属性添加到user当中
    
    # 如果user没有portrait属性  则添加
    if not hasattr(user,'portrait'):
        cmsuser = CmsUser.objects.filter(user__pk=user.pk).first()
        if cmsuser:
            # 三个属性，给谁添加 添加什么属性 属性值
            setattr(user,'portrait',cmsuser.portrait)

    return {'user':user}
