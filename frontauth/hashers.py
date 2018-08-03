# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2017-01-22 10:22:25
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 23:06:26
import hashlib
import configs

def make_password(raw_password,salt=None):
    if not salt:
        # 加密 并转为16进制
        salt = configs.PASSWORD_SALT
        
    hash_password = hashlib.md5(salt + raw_password).hexdigest()
    return hash_password

def check_password(raw_password,hash_password):
        # 首先对raw_password进行加密 再进行对比
        if not raw_password:
            return False

        tmp_password = make_password(raw_password) 

        # 如果此刻加密后的密码与 数据库中已加密的密码相同 验证成功
        if tmp_password == hash_password:
            return True
        else:
            return False