/*
* @Author: Mack
* @Date:   2017-01-19 09:20:21
* @Last Modified by:   56958
* @Last Modified time: 2017-02-27 20:07:18
*/

'use strict';
$(function(){
    var url = window.location.href;
    // http://127.0.0.1:9000/article_list/4
    // http:  127.0.0.1:8000 article_list 2
    // 有两种情况：
    // 1. 处在所有文章页面的时候，categoryId无需获取，只需给第1个li添加active类
    // 2. 处在其他类，需解析url，然后从第4个位置获取category_id
    if (url.indexOf('article_list')>0) {
        // 将url解析 获取categoryId
        var urlArray = url.split('/');
        var categoryId = urlArray[4];
        // 判断当前哪个children 的 data-category-id 与 categoryId 相等 取出
        var liTag = $('#category-box').children('[data-category-id='+categoryId+']');
        liTag.addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('article_detail')>0){

        // 详情页面对应的分类 active项
        var categoryId = $('h2.article-title').attr('data-category-id');
        // console.log(categoryId);
        var liTag = $('#category-box').children('[data-category-id='+categoryId+']');
        liTag.addClass('active').siblings().removeClass('active');
    } else {
        // 不存在article_list 直接给eq(0)添加 active
        $('#category-box').children().eq(0).addClass('active').siblings().removeClass('active');
    }
});