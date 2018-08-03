# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:27:00
# @Last Modified by:   56958
# @Last Modified time: 2017-03-12 13:18:13
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from forms import *
from django.shortcuts import render,redirect,reverse
from cmsauth.models import CmsUser
from qiniu import Auth,put_file
from django.core.cache import cache
import qiniu.config
from django.views.decorators.http import require_http_methods
from django.core import mail
import hashlib,time
from article.models import CategoryModel,ArticleModel,TagModel,TopModel
from utils import myjson
from django.conf import settings
from django.forms import model_to_dict
# 导入计算文章篇数函数
from django.db.models import Count
from utils.myemail import send_email

def cms_login(request):
    if request.method == 'GET':
        return render(request,'cms_login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username',None)
            password = form.cleaned_data.get('password',None)
            remember = form.cleaned_data.get('remember',None)
            # 1. 先用authenticate进行验证
            user = authenticate(username=username,password=password)
            if user:
                # 2. 需要登录,
                # 3. 我们的login视图函数不要和login重名
                login(request,user)
                # 记住我
                if remember:
                    request.session.set_expiry(120)
                else:
                    # 只要关闭浏览器(不是网页) 则过期
                    request.session.set_expiry(0)                    
                nexturl = request.GET.get('next')
                if nexturl:
                    return redirect(nexturl)
                else:
                    return redirect(reverse('cms_index'))
            else:
                return render(request,'cms_login.html',{'error':u'用户名或密码错误!'})
        else:
            return render(request,'cms_login.html',{'error':form.get_error()})

# 登出函数
def cms_logout(request):
    logout(request)
    return redirect(reverse('cms_login'))


def cms_settings(request):
    # 1.修改用户名
    # 2.修改头像
    # 3.修改邮箱
    return render(request,'cms_settings.html')



@login_required
@require_http_methods(['POST'])
def update_profile(request):
    # 1.更新头像
    # 2.更新用户名
    form = UpdateProfileForm(request.POST)
    if form.is_valid():
        portrait = form.cleaned_data.get('portrait',None)
        username = form.cleaned_data.get('username',None)
        # user = request.user # 中间件设置当前的user到request上
        user = User.objects.all().first()
        user.username = username
        user.save()
        cmsuser = CmsUser.objects.filter(user__pk=user.pk).first()
        # 如果CmsUser表中已存在数据与user对应 直接更新
        if cmsuser:
            cmsuser.portrait = portrait
        # 否则，先新建一个cmsuser模型 再保存
        else:
            cmsuser = CmsUser(portrait=portrait,user=user)
        cmsuser.save()
        # return JsonResponse({'code':200})
        return myjson.json_result()
    else:
        # return JsonResponse({'error':form.errors})
        return myjson.json_params_error(message=u'表单验证错误！')



# @login_required
@require_http_methods(['POST'])
def add_category(request):
    form = AddCategoryForm(request.POST)
    if form.is_valid():
        print '-------------------sucece'
        categoryname = form.cleaned_data.get('categoryname',None)
        resultCategory = CategoryModel.objects.filter(name=categoryname).first()
        if not resultCategory:
            categoryModel = CategoryModel(name=categoryname)
            categoryModel.save()
            # return JsonResponse(data={'id':categoryModel.id,'name':categoryModel.name,'code':200})
            return myjson.json_result(data={'id':categoryModel.id,'name':categoryModel.name})
        else:
            # return JsonResponse({'error':u'该分类已存在！','code':400})
            return myjson.json_params_error(message=u'该分类已存在！')
    else:
        print '---------------------error'
        # return JsonResponse({'error':form.errors.as_json,'code':'400'})
        return myjson.json_params_error(message=u'表单验证错误！')

@login_required
@require_http_methods(['POST'])
def add_tag(requset):
    form = AddTagForm(requset.POST)
    if form.is_valid():
        tagname = form.cleaned_data.get('tagname',None)
        resultTag = TagModel.objects.filter(name=tagname).first()
        if not resultTag:
            tagModel = TagModel(name=tagname)
            tagModel.save()
            # return JsonResponse(data={'id':tagModel.id,'name':tagModel.name,'code':200})
            return myjson.json_result(data={'id':tagModel.id,'name':tagModel.name})
        else:
            # return JsonResponse({'error':u'该标签已存在！','code':400})
            return myjson.json_params_error(message=u'该标签已存在！')
    else:
        # return JsonResponse({'error':form.errors.as_json,'code':'403'})
        return myjson.json_params_error(message=u'表单验证错误！')

@login_required
@require_http_methods(['GET'])
def get_token(request):
    """
    1.客户端在上传图片到七牛之前,需要从业务服务器上获取token,本函数就是获取token    
    2.客户端获取到token后,将token与图片一起上传到七牛服务器
    3.七牛收到token和图片后,会判断当前token是否有效,如果有效,则返回图片名到客户
    端和业务服务器
    """

    # 1. 设置AccessKey 和 SecretKey  
    AccessKey = 'T4d1rxhOBKR6PmvdIY4FuU38pgQ2Z9m0kZq2ORJF'
    SecretKey = 'u3T7Q19Uorl349gWALxz7bEo-PRGNkwwyYHUKgV6'
    # 2. 授权
    q = Auth(AccessKey,SecretKey)
    # 3. 设置七牛空间 
    bucket_name = 'mack'
    # 4.生成token
    token = q.upload_token(bucket_name)
    # 5.返回token,且key必须为'uptoken'
    # return JsonResponse({'uptoken':token})
    return myjson.json_result(kwargs={'uptoken':token})


@login_required
@require_http_methods(['GET','POST'])
def update_email(request):
    if request.method == 'GET':
        return render(request,'cms_email.html')
    else:
        form = UpdateEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email',None)
            # 如果邮箱存在
            if email:
                if send_email(request,email,'cms_check_email'):
                    return redirect(reverse('cms_success_email'))
                else:
                    return redirect(reverse('cms_fail_email'))
        else:
            return render(request,'cms_email.html',{'error':form.errors})
            # 如果邮箱不存在
              # return redirect(reverse('cms_find_email'))

# 发送邮件成功
@login_required
@require_http_methods(['GET'])
def success_email(request):
    return render(request,'cms_email_success.html')

# 发送邮件失败
@login_required
@require_http_methods(['GET'])
def fail_email(request):
    return render(request,'cms_email_fail.html')

# 邮箱不存在
@login_required
@require_http_methods(['GET','POST'])
def find_email(request):
    return  render(request,'cms_email_check.html')

@login_required
@require_http_methods(['GET'])
def check_email(request,code):
    """
        验证邮箱的url
    """
    # 需要知道原邮箱
    # http://127.0.0.1:8000/cms/check_email/
    if len(code) > 0:
        # 通过code获取缓存中的email
        email = cache.get(code)
        if email:
            user = request.user
            user.email = email
            user.save(update_fields=['email'])      # 指定需要保存的字段  提升效率
            return HttpResponse(u'恭喜您！邮箱通过验证！')
        else:
            return HttpResponse(u'对不起！该链接已失效！')
    else:
        return HttpResponse(u'对不起！该链接已失效！')


# 文章相关操作

# 管理文章
@login_required
def article_manage(request,page=1,category_id=0):
    # page   c_page    t_page
    currentPage = int(page) # 当前页面
    # 取出分类id
    categoryId = int(category_id)
    numPage = int(settings.NUM_PAGE) # 每页文章数
    # 判断当前分类 若categoryId > 0 则按分类选取 否则 显示全部
    if categoryId > 0:
        articles = ArticleModel.objects.all().filter(category__pk=categoryId).order_by('-top__Alter_time','-public_date')
    else:
        articles = ArticleModel.objects.all().order_by('-top__Alter_time','-public_date')

    start = (currentPage-1)*numPage # 每页起始文章编码
    end = start+numPage # 每页末尾文章编码
    
    # 文章总数
    articleCount = articles.count()
    # 对文章进行切片
    articles = articles[start:end]
    # 总页数
    pageCount = articleCount/numPage
    if articleCount%numPage != 0:
        pageCount += 1
    # 存放在数组中的页码nav
    pages = []
    
    # (1,2,[3],4,5)
    # 往前找 
    tmpPage = currentPage - 1 # [3]-1 == 2
    # 2 >=1时 
    while tmpPage >= 1:
        # 如果当前页面能被5整除 应换页
        if tmpPage % 5 == 0:
            break
        else:
            pages.append(tmpPage)
            tmpPage -= 1

    # (1,2,[3],4,5)
    # 往后找
    tmpPage = currentPage # [3]
    while tmpPage <= pageCount:
        if tmpPage % 5 == 0:
            pages.append(tmpPage)
            break
        else:
            pages.append(tmpPage) 
            tmpPage += 1

    # 给pages排序
    pages.sort()
    # print(pages)
    # 要传入的context

    # 获取分类
    categorys = CategoryModel.objects.all() 

    context = {
        't_page':pageCount,
        'c_page':currentPage,
        'pages':pages,
        'articles':articles,
        'categorys':categorys,
        'c_category':categoryId
    }
    return render(request,'cms_article_manage.html',context=context)

# 添加文章
@login_required
def add_blog(request):
    if request.method == 'GET':
        categorys = CategoryModel.objects.all()
        tags = TagModel.objects.all()
        data = {
            'categorys':categorys,
            'tags':tags,
        }
        return render(request,'cms_addarticle.html',data)
    else:
        form = AddArticleForm(request.POST)
        if form.is_valid():
            # print('success.....')
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content_html = form.cleaned_data.get('content_html')
            tags = request.POST.getlist('tags[]')
            # print(tags)
            user = request.user
            categoryModel = CategoryModel.objects.filter(pk=category).first()
            articleModel = ArticleModel(title=title,desc=desc,thumbnail=thumbnail,content_html=content_html,author=user,category=categoryModel)
            articleModel.save()
            # 添加tags的多对多
            for tag in tags:
                tagModel = TagModel.objects.filter(pk=tag).first()
                if tagModel:
                    articleModel.tags.add(tagModel)
            
            return myjson.json_result(data={})
        else:
            # print('error..........')
            return form.get_error_response()

# 删除文章
@login_required
@require_http_methods(['POST'])
def delete_blog(request):
    form = DeleteArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articleModel = ArticleModel.objects.filter(pk=uid).first()
        if articleModel:
            articleModel.delete()
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'该文章不存在！')
    else:
        return form.get_error_response()


# 编辑文章
@login_required
@require_http_methods(['GET','POST'])
def edit_blog(request,pk=''):
    if request.method == 'GET':
        article = ArticleModel.objects.filter(pk=pk).first()
        # 通过moel_to_dict 转换为 dict
        articleDict = model_to_dict(article)
        # 取dict中key['tags']的值 设为列表
        articleDict['tags'] = []
        # print(type(articleDict))  --dict
        # print(articleDict)  --QuerySet

        # 将其转化为id并存入articleDict中
        for tagModel in article.tags.all():
            articleDict['tags'].append(tagModel.id)

        # print(articleDict)

        context = {
            'article': article,
            # 保存标签,另起一个Dict存放
            'Dict':articleDict,
            'categorys':CategoryModel.objects.all(),
            'tags':TagModel.objects.all(),
        }
        return render(request,'cms_edit_article.html',context)
    else:
        form = UpdateArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content_html = form.cleaned_data.get('content_html')
            tags = request.POST.getlist('tags[]')
            uid = form.cleaned_data.get('uid')
            articleModel = ArticleModel.objects.filter(pk=uid).first()
            if articleModel:
                # 更新文章各项数据
                # articleModel.uid = uid
                articleModel.title = title
                articleModel.desc = desc
                articleModel.thumbnail = thumbnail
                articleModel.content_html = content_html
                articleModel.category = CategoryModel.objects.filter(pk=category).first()
                articleModel.save()

                if tags:
                    for tag in tags:
                        tagModel = TagModel.objects.filter(pk=tag).first()
                        articleModel.tags.add(tagModel)
            return myjson.json_result()
        else:
            return form.get_error_response()


# 置顶文章
@login_required
@require_http_methods(['POST'])
def top_blog(request):
    form = TopArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articleModel = ArticleModel.objects.filter(pk=uid).first()
        # 如果文章存在
        if articleModel:
            topModel = articleModel.top
            if not topModel:
                # 如果未置顶 生成一个TopModel并保存
                topModel = TopModel()
            # 已置顶 也save，确保alter_time为最新
            topModel.save()
            articleModel.top = topModel
            articleModel.save(update_fields=['top'])
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'该文章不存在！')
    else:
        return form.get_error_response()

# 取消置顶
@login_required
@require_http_methods(['POST'])
def untop_blog(request):
    form = TopArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articleModel = ArticleModel.objects.filter(pk=uid).first()
        # 如果文章存在
        if articleModel:
            if articleModel.top:
                topModel = articleModel.top
                topModel.delete()
                return myjson.json_result()
            else:
                return myjson.json_params_error(message=u'该文章未置顶！')
        else:
            return myjson.json_params_error(message=u'该文章不存在！')
    
    else:
        return form.get_error_response()


# 分类管理操作
@login_required
@require_http_methods(['GET'])
def category_manage(request):
    if request.method == 'GET':
        # annotate 会给QuerySet中所有模型添加 聚合函数提供的属性 如下
        categorys = CategoryModel.objects.all().annotate(num_articles=Count('articlemodel')).order_by('-num_articles')
        
        # 打印出 分类categorys[0]中的文章数量 __count
        # print categorys[0].num_articles,categorys[0].name
        context = {
            'categorys':categorys
        }
        return render(request,'cms_category_manage.html',context)

# 编辑分类
@login_required
@require_http_methods(['POST'])
def edit_category(request):
    form = EditCategoryForm(request.POST)
    if form.is_valid():
        categoryId = form.cleaned_data.get('category_id')
        cateName = form.cleaned_data.get('name')
        categoryModel = CategoryModel.objects.filter(pk=categoryId).first()

        if categoryModel:
            categoryModel.name = cateName
            categoryModel.save(update_fields=['name'])
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'不存在该分类！')
    else:
        return form.get_error_response()

# 删除分类
@login_required
@require_http_methods(['POST'])
def delete_category(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        categoryId = form.cleaned_data.get('category_id')
        categoryModel = CategoryModel.objects.filter(pk=categoryId).first()

        if categoryModel:
            # 首先获取该分类下文章数量
            articleCount = categoryModel.articlemodel_set.all().count()
            # 若该分类存在文章 禁止删除操作
            if articleCount > 0:
                return myjson.json_params_error(message=u'无法删除该分类,请删除分类下文章后再尝试')
            else:
                categoryModel.delete()
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'不存在该分类！')
    else:
        return form.get_error_response()

# 评论管理操作

@login_required
@require_http_methods(['POST'])
def comment_manage(request):
    pass

























# 测试
def test(request):
    for x in xrange(21,40):
        title = u'代码%s' % x
        # 查找id为1的
        category = CategoryModel.objects.get(id=3)
        content_html = u'代码 %s' % x
        articleModel = ArticleModel(title=title,content_html=content_html,category=category)
        articleModel.save()
    return myjson.json_result()