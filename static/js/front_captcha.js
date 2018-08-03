/*
* @Author: Mack
* @Date:   2017-01-22 21:37:32
* @Last Modified by:   Mack
* @Last Modified time: 2017-01-22 21:37:35
*/

'use strict';
$(function(){
    $('.captcha-img').click(function(){
        // ajax擅长处理纯文本和json对象
        // 对于流媒体不擅长,比较消耗资源
        // img的src发生改变,则重新加载图片
        var old_src = $(this).attr('src');
        var src = old_src + '?xx=' + Math.random();
        $(this).attr('src',src);
    });
});