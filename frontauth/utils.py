# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2017-01-22 11:02:33
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 19:52:00
from models import FrontUserModel
import configs
def login(request,email,password):
    # 传request是为了做一些登陆的数据设置
    # 1. 获取用户的数据进行验证
    user = FrontUserModel.objects.filter(email=email).first()
    if user:
        result = user.check_password(password)
        # 2. 验证通过 在session中保存当前用户信息 下次登陆时 直接从session中获取用户信息 
        #    获取不到 说明没有登录
        if result:
            # print '-'*30
            # print type(str(user.pk))
            # print '-'*30
            request.session[configs.LOGINED_KEY] = str(user.pk)
            return user
        else:
            return None
    else:
        return None


def logout(request):
    """
        退出登录
    """
    try:
        del request.session[configs.LOGINED_KEY]
    except KeyError:
        pass