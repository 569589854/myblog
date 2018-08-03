# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:26:53
# @Last Modified by:   Mack
# @Last Modified time: 2017-01-22 22:24:37
from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^$',views.article_manage,name='cms_index'),
    url(r'^login/',views.cms_login,name='cms_login'),
    url(r'^logout/',views.cms_logout,name='cms_logout'),
    url(r'^addblog/',views.add_blog,name='cms_addblog'),
    url(r'^editblog/(?P<pk>[\w\-]+)',views.edit_blog,name='cms_editblog'),
    url(r'^deleteblog/',views.delete_blog,name='cms_deleteblog'),
    url(r'^topblog/',views.top_blog,name='cms_topblog'),
    url(r'^untopblog/',views.untop_blog,name='cms_untopblog'),
    url(r'^article_manage/(?P<page>\d+)/(?P<category_id>\d+)',views.article_manage,name='cms_article_manage'),
    url(r'^category_manage/',views.category_manage,name='cms_category_manage'),
    url(r'^comment_manage/',views.comment_manage,name='cms_comment_manage'),
    url(r'^add_category/',views.add_category,name='cms_add_category'),
    url(r'^edit_category/',views.edit_category,name='cms_edit_category'),
    url(r'^delete_category/',views.delete_category,name='cms_delete_category'),
    url(r'^settings/',views.cms_settings,name='cms_settings'),
    url(r'^update_profile/',views.update_profile,name='cms_update_profile'),
    url(r'^update_email/',views.update_email,name='cms_update_email'),
    url(r'^check_email/(?P<code>\w+)',views.check_email,name='cms_check_email'),
    url(r'^success_email/',views.success_email,name='cms_success_email'),
    url(r'^fail_email/',views.fail_email,name='cms_fail_email'),
    url(r'^find_email/',views.find_email,name='cms_find_email'),
    url(r'^get_token/',views.get_token,name='cms_get_token'),
    url(r'^add_tag/',views.add_tag,name='cms_add_tag'),
    url(r'^test/',views.test),
]
