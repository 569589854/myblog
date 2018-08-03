/*
* @Author: Mack
* @Date:   2017-01-19 22:31:44
* @Last Modified by:   Mack
* @Last Modified time: 2017-01-20 21:30:28
*/

'use strict';
$(function(){
    $('.load-more-btn').click(function(){
        var self = $(this);
        // 加载未完成时显示内容
        self.button('loading');
        var cPage = parseInt($(this).attr('data-page-id'));
        var page = cPage + 1;
        var categoryId = $(this).attr('data-category-id');
        if (!categoryId){
            categoryId = 0;
        };
        var url = '/article_list/' + categoryId +'/' + page + '/';
        my_ajax.get({
            'url':url,
            'success':function(result){
                if(result['code']==200){
                    //将文章列表追加到ul后面
                    var articles = result['data']['articles'];
                    if (articles.length == 0){
                        self.html('没有更多文章');
                        self.attr('disabled','disabled');
                    }else{
                        for (var i = 0; i < articles.length; i++) {
                            var article = articles[i];
                            if(!article['desc']){
                                var content_html = article['content_html']; 
                                // 过滤掉加粗 红色字体等
                                content_html = $(content_html).text();
                                if(!content_html){
                                    content_html = article['content_html'];
                                }
                                content_html = content_html.substr(0,100) + '...';
                                article['desc'] = content_html;
                            }
                            // 引用xttemplate中封装的 时间格式函数 更改时间格式
                            var html = xttemplate.template('front-article-tpl',{'article':article});
                            $('#article-list-box').append(html);
                        }
                        // 更改当前页面
                        self.attr('data-page-id',page);
                        self.button('reset');
                    }
                }else{
                    return result['message']
                }
            },
            'error':function(error){
                alert(error);
            }
        });
    });
});