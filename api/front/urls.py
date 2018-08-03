# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:27:59
# @Last Modified by:   56958
# @Last Modified time: 2017-03-11 22:48:18
from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$',views.article_list,name='front_index'),
    url(r'^signin',views.signin,name='front_signin'),
    url(r'^signup',views.signup,name='front_signup'),
    url(r'^update_profile/',views.update_profile,name='front_update_profile'),
    url(r'^signout',views.signout,name='front_signout'),
    url(r'^forget_password',views.forget_password,name='front_forget_password'),
    url(r'^reset_password/(?P<code>\w+)',views.reset_password,name='front_reset_password'),
    url(r'^check_email/(?P<code>\w+)',views.check_email,name='front_check_email'),
    url(r'^article_list/(?P<category_id>\d+)/(?P<page>\d+)',views.article_list,name='front_article_list'),
    url(r'^article_detail/(?P<article_id>[\w\-]+)',views.article_detail,name='front_article_detail'),
    url(r'^settings/',views.front_settings,name='front_settings'),
    url(r'^get_token/',views.get_token,name='front_get_token'),
    url(r'^comment/',views.comment,name='front_comment'),
    url(r'^search',views.cms_search,name='front_search'),
]
