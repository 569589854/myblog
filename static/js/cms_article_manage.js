/*
* @Author: Mack
* @Date:   2017-01-14 20:18:37
* @Last Modified by:   56958
* @Last Modified time: 2017-02-27 20:06:45
*/

'use strict';
// 分页按钮disabled
$(function(){
    $('.disabled').click(function(event){
        // 阻止a标签默认行为
        event.preventDefault();
    });
});

// 删除文章
$(function(){
    $('.delete-article-btn').click(function(event){
        //阻止a标签默认行为
        event.preventDefault();
        var result = confirm("您确定要删除这篇文章吗？");
        if (result) {
            var tdTag = $(this).parent();
            var uid = tdTag.attr('data-article-id');    
            my_ajax.post({
                'url':'/cms/deleteblog/',
                'data':{
                    'uid':uid
                },
                'success':function(result){
                    if (result['code'] == 200) {
                        tdTag.parent().hide(1000,function(){
                            tdTag.parent().remove();
                        });
                    } else {
                        alert(result['message'])
                    }
                },
                'error':function(error){
                    alert(error);
                }
            });
        } else {

        }
    });
});

// 置顶与取消文章
$(function(){
    $('.top-article-btn').click(function(event){
        event.preventDefault();
        var self = $(this);
        var tdTag = $(this).parent();
        var uid = tdTag.attr('data-article-id');
        var url = '/cms/topblog/';
        if(self.html().indexOf('取消置顶')>=0){
            url = '/cms/untopblog/';
        }
        my_ajax.post({
            'url':url,
            'data':{
                'uid':uid
            },
            'success':function(result){
                if (result['code'] == 200) {
                    // console.log('200');
                    // 1.标题前添加[置顶]
                    // var span = $('<span class="top-title-word">[置顶]</span>');
                    // // 若用this是指 success,
                    // var titleTag = self.parent().siblings().first().children().eq(0);
                    // // console.log(titleTag);
                    // var title = titleTag.text(); //标题名称
                    // // console.log(title);
                    // titleTag.html(''); //span标签置空
                    // titleTag.append(span);
                    // titleTag.append(title);
                    // console.log(title)

                    //直接重新载入页面即可
                    window.location = '/cms/';
                    
                    // 2.修改为 "取消置顶"   
                    self.text('取消置顶');
                } else {
                    alert(result['message'])
                }
            },
            'error':function(error){
                alert(error);
            }
        });
    });
});

// 分类
$(function(){
    // 监听分类是否改变
    $('#category-select').change(function(){
        var category_id = $(this).val();
        window.location = '/cms/article_manage/1/' + category_id + '/';
    });
});