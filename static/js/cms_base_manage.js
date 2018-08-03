/*
* @Author: Mack
* @Date:   2017-01-16 18:05:00
* @Last Modified by:   Mack
* @Last Modified time: 2017-01-16 18:20:26
*/

'use strict';

$(function(){
    var url = window.location.href;
    var ulTag = $('#sub-nav');
    var index = 0;
    if (url.indexOf('category_manage') > 0) {
        index = 1;
    }else if(url.indexOf('comment_manage') > 0){
        index = 2;
    }else{
        index = 0; 
    }
    ulTag.children().eq(index).addClass('active').siblings().removeClass('active');
});