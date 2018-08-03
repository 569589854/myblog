/*
* @Author: Mack
* @Date:   2017-01-13 20:20:54
* @Last Modified by:   56958
* @Last Modified time: 2017-02-27 20:07:48
*/

'use strict';

// var args = {'browse_button':'thumbnail-btn','success':function(){},'error':function(){}};
// qiniu.setUp(args);
var myqiniu = {
    'setUp': function(args){
        var domain = 'http://ogoriukjl.bkt.clouddn.com/';
        var params = {
            runtimes: 'html5,flash,html4', //上传模式，依次退化
            max_file_size: '500mb', //文件最大允许的尺寸
            dragdrop: false, //是否开启拖拽上传
            chunk_size: '4mb', //分块上传时，每片的大小
            // uptoken_url: '/cms/get_token/', //ajax请求token的url
            domain: domain, //图片下载时候的域名
            get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
            auto_start: true, //true，只要选择了图片，则自动上传
            log_level: 5, //log级别
            init:{
                'FileUploaded': function(up,file,info) {
                    if (args['success']) {
                        var success = args['success'];
                        file.name = domain + file.name;
                        // console.log(file.name);
                        success(up,file,info);
                    }
                },
                'Error': function(up,err,errTip) {
                    if (args['error']) {
                        var error = args['error'];
                        error(up,err,errTip);
                    }
                },
            },
        };    
        //更新params
        for (var key in args) {
            params[key] = args[key]; 
        } //....此时多了2个  success:function,error:function;
        // console.log(params);
        //执行uploader操作
        var uploader = Qiniu.uploader(params);
        return uploader;
    }
}