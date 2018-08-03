/*
* @Author: Mack
* @Date:   2017-01-16 16:49:40
* @Last Modified by:   Mack
* @Last Modified time: 2017-01-16 18:02:31
*/

'use strict';
// 编辑操作
$(function(){
    var dialog = $("#category-modal");
    $(".edit-category-btn").click(function(event){
        event.preventDefault();
        // 弹出框
        dialog.modal('show');
        var categoryId = $(this).parent().parent().attr('data-category-id');
        // 将categoryId绑定到弹出框
        $("#alter-confirm-btn").attr('data-category-id',categoryId);
    });
    $("#alter-confirm-btn").click(function(){
        var categoryId = $("#alter-confirm-btn").attr('data-category-id');
        // 弹出框输入名称
        var name = $("#category-input").val();
        // console.log('categoryId:'+categoryId+',name:'+name);
        my_ajax.post({
            'url':'/cms/edit_category/',
            'data':{
                'category_id':categoryId,
                'name':name
            },
            'success':function(result){
                if(result['code']==200){
                    // 修改当前分类标题
                    // 遍历tr标签
                    $('.category-tr').each(function(){
                        // 若此tr标签的 data-category-id 属性 == category的id
                        if ($(this).attr('data-category-id') == categoryId) {
                            // 修改名称
                            // name属性
                            $(this).children().eq(0).html(name);
                        }
                    });
                }else{
                    console.log(result['message']);
                }
            },
            'error':function(result){
                alert(error);
            },
            'complete':function(result){
                dialog.modal('hide');
            }
        });
    });
});

// 删除操作
$(function(){
    $('.delete-category-btn').click(function(event){
        event.preventDefault();
        var trTag = $(this).parent().parent();
        var categoryId = trTag.attr('data-category-id');
        var result = confirm("您确定要删除该分类吗？");
        if (result) {
            my_ajax.post({
                'url':'/cms/delete_category/',
                'data':{
                    'category_id':categoryId,
                },
                'success':function(res){
                    if(res['code']==200){
                        // 渐变式删除该分类
                        trTag.hide(1000,function(){
                            $(this).remove();
                        }); 
                    }else{
                        alert(res['message']);
                    }
                },
                'error':function(error){
                    console.log(error);
                }
            });
        }
    });
});