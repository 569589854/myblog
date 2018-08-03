# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2017-01-22 21:01:11
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 21:13:42
import configs
from models import FrontUserModel
def auth(request):
    # 给模板添加一个front_user变量
    # 1.若已登录 添加front_user变量
    if request.session.get(configs.LOGINED_KEY):
        # 2.若已登录 且存在front_user 
        if hasattr(request,'front_user'):
            return {'front_user':request.front_user}
        # 3.若已登录 但无front_user 需从数据库中获取user对象
        else:
            uid = request.session.get(configs.LOGINED_KEY)
            user = FrontUserModel.objects.filter(pk=uid).first()
            return {'front_user':user}
    # 2.若未登录 返回空子典
    else:
        return {}