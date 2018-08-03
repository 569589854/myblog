/*
* @Author: Mack
* @Date:   2016-11-01 22:58:11
* @Last Modified by:   Mack
* @Last Modified time: 2016-11-07 11:19:06
*/

'use strict';
$(document).ready(function(){
    // 1.获取当前URL
    var c_url = window.location.href;
    // 2.判断当前URL是哪个,再给具体指定的li添加 active 类
    var c_index = 0;
    // 判断当前url是否包含addarticle
    if(c_url.indexOf('addblog')>0){
        c_index = 1;
    }else if(c_url.indexOf('settings')>0){
        c_index = -1;
    }else{
        c_index = 0;
    }
    var ulTag = $('.menu-ul');
    if (c_index >= 0){
        ulTag.children().eq(c_index).addClass('active').siblings().removeClass('active');
    }else{
        ulTag.children().removeClass('active');
    }
});

// 此法应在所有images之类的加载完毕后才执行
// $(function(){
//     // 1.获取当前URL
//     var c_url = window.location.href;
//     // 2.判断当前URL是哪个,再给具体指定的li添加 active 类
//     var c_index = 0;
//     // 判断当前url是否包含addarticle
//     if(c_url.indexOf('addblog')>0){
//         c_index = 1;
//     }else{
//         c_index = 0;
//     }
//     var ulTag = $('.menu-ul');
//     ulTag.children().eq(c_index).addClass('active').siblings().removeClass('active');
// });