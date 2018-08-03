/*
* @Author: Mack
* @Date:   2016-11-07 19:00:09
* @Last Modified by:   56958
* @Last Modified time: 2017-02-27 20:05:13
*/
'use strict';
$(function() {
    //初始化七牛SDK代码
    //初始化七牛的代码必须放在选择图片行为之前
        var uploader = myqiniu.setUp({
        'browse_button': 'pickfiles',
        'uptoken_url': '/cms/get_token/',
        //其实就是调用init中的FileUploaded(up,file,info)和Error(up,file,errTip),换了函数名,不能改名
        'success': function(up,file,info) {
            // console.log('file uploaded-----------');
            //把图片URL设置进img标签
            $('#pickfiles').attr('src',file.name)
        },
        'error': function(up,err,errTip) {
            // console.log('error:'+err);
        },
    });

    //提交按钮执行事件
    $('.submit-btn').click(function (event) {
        event.preventDefault();//阻止默认行为
        var username = $('.username-input').val();
        var portrait = null; 
        //如果有图片上传
        if(uploader.files.length > 0){
            //src就是上传图片的url
            portrait = $('#pickfiles').attr('src');
        }
        var data = {'username':username};
        //有图片更新

        if(portrait){
            data['portrait'] = portrait;
        }
        my_ajax.post({
            'url':'/cms/update_profile/',
            'data':data,
            'success':function(data){
                if (data['code'] == 200) {
                    // 重新加载页面 刷新信息
                    document.location.reload();
                    var alert = $('.alert-success')
                    alert.html('更新成功');
                    alert.show();
                }
            },
            'error':function(error){
                // console.log(error);
            },
        });
    });
});