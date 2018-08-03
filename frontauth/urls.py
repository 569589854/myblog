# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2017-01-22 09:37:21
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 20:57:23
from django.conf.urls import url,include
import views
urlpatterns = [
    url(r'^add_user',views.add_user),
    url(r'^test1',views.test1),
    url(r'^front_login',views.front_login),
    url(r'^front_logout',views.front_logout),
    url(r'^check_login',views.check_login),
    url(r'^decorator_check',views.decorator_check),
    url(r'^middleware_test',views.middleware_test),
]
