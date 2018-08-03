/*
* @Author: Mack
* @Date:   2016-11-21 10:51:29
* @Last Modified by:   56958
* @Last Modified time: 2017-02-27 20:06:44
*/

'use strict';
// 初始化simditor的函数
$(function() {
    var editor,toolbar;
    toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough', 'fontScale', 'color', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'image', 'hr', '|', 'indent', 'outdent', 'alignment'];
    Simditor.locale = 'zh-CN';
    editor = new Simditor({
        textarea: $('#simditor'),
        toolbar: toolbar,
        pasteImage: true
    });
    // 加到window上去,其他地方才能访问到editor这个变量
    window.editor = editor;
});

$(function(){
    var dialog = $('#category-modal');
    $('#category-btn').click(function() {
        dialog.modal('show');
    });
    $('#category-save-btn').click(function() {
        //1.获取输入框中的值
        var categoryInput = $('#category-input');
        var categoryname = categoryInput.val();
        // 控制台打印
        // console.log(categoryname)
        //2.提交到服务器
        my_ajax.post({
            'url': '/cms/add_category/',
            'data': {'categoryname':categoryname},
            'success':function(result){
                //在控制台输出请求详细信息
                // console.log(result['data'])
                if (result['code'] == 200){
                    //请求成功
                    var data = result['data'];
                    var select = $('#category-select');
                    dialog.modal('hide');
                    var option = $('<option></option>')
                    option.attr('value',data['id']);
                    option.html(data['name'])
                    // 通过append添加进去的,一定是在最后面
                    select.append(option);
                    // 可以通过last方法获取到刚刚添加进去的option
                    select.children().last().attr('selected','selected').siblings().removeAttr('selected');
                }else{

                }
            },
            'error':function(error){
                console.log(error);
            }
        })
    });

    var taglog = $('#tag-modal');
    $('#tag-btn').click(function(){
        taglog.modal('show');
        // var tpl = template('cms_tag_template',{'id':'16','name':'Java'});
        // console.log(tpl)
    });
    //创建lebel标签的函数
    function addLabelTag(){
        var label = $('<label class="checkbox-inline"></label>');
        var input = $('<input type="checkbox" />');
        // input.attr('value',data['id']);
        input.val(data['id'])
        input.attr('check','checked');
        label.append(input);
        label.append(data['name'])
        $("#tag-box").append(label);
    };
    $('#tag-add-btn').click(function(){
        //1.获取输入框中的值
        var tagInput = $('#tag-input');
        var tagname = tagInput.val();
        // console.log(tagname);
        //2.提交到服务器
        my_ajax.post({
            'url':'/cms/add_tag/',
            'data':{'tagname':tagname},
            'success':function(result){
                //在控制台输出请求的详细信息
                // console.log(result['data']);
                if(result['code'] == 200){
                    //请求成功
                    var data = result['data'];
                    // 1.第一种方式通过jquery原始dom操作创建新的label和input标签
                    // addLabelTag();

                    // 2.第二种方式通过arttemplate模板的方式进行创建，同样获取输入框中内容
                    var tpl = template('cms_tag_template',{'id':data['id'],'name':data['name']});
                    $("#tag-box").append(tpl);
                    taglog.modal('hide');
                }else{
                    console.log(result['message'])
                }
            },
            'error':function(error){
                console.log(error);
            }
        })
    });
});

//上传图片执行函数
$(function(){
    var uploader = myqiniu.setUp({
        'browse_button':'thumbnail-btn',
        //其实就是调用init中的FileUploaded(up,file,info)和Error(up,file,errTip),换了函数名
        'success':function(up,file,info){
            //把图片URL设置进imput标签
            $('#thumbnail-input').val(file.name);
        },
        'error':function(up,file,errTip){
            console.log(err);
        }  
    });
});

//发布文章函数
$(function(){
    $('#submit-btn').click(function(){
        //获取元素
        var titleElement = $('#title-input');
        var categoryElement = $('#category-select');
        var descElement = $('#descinput');
        var thumbnailElement = $('#thumbnail-input');
        var tagElements = $('.tag-input');
        var content_html = editor.getValue();
        var tags = [];

        //获取数据
        var title = titleElement.val();
        var category = categoryElement.val();
        var desc = descElement.val();
        var thumbnail = thumbnailElement.val();
        tagElements.each(function(){
            if($(this).is(':checked')){
                var tagId = $(this).val();
                tags.push(tagId);
            }
        });
        // console.log(tags);
        var data = {
            'title':title,
            'category':category,
            'desc':desc,
            'thumbnail':thumbnail,
            'tags[]':tags,
            'content_html':content_html,
            'uid':titleElement.attr('data-article-id')
        };
        // console.log(data)
        //通过ajax发送到服务器
        my_ajax.post({
            'url':window.location.href,
            'data':data,
            'success':function(result){
                if (result['code']==200) {
                    // console.log('200')
                    $('#submit-success-modal').modal('show');
                    titleElement.val('');
                    categoryElement.val('');
                    descElement.val('');
                    thumbnailElement.val('');
                    tagElements.removeAttr('checked');
                    editor.setValue('');
                    // console.log('传送完毕!')
                } else {
                    console.log('500')
                    console.log(result['message']);
                }
            },
            'error':function(err){
                console.log(err);
            }
        });
    });
    $('#back-to-home').click(function(){
        //地址设为首页
        window.location = '/cms';
    });
    $('#write-another-one').click(function(){
        //已做清空处理  只需隐藏提示框
        $('#submit-success-modal').modal('hide');
    });
});