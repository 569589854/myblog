# -*- coding: utf-8 -*-
# @Author: Mack
# @Date:   2016-11-01 19:28:06
# @Last Modified by:   56958
# @Last Modified time: 2017-03-11 22:48:06
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect,reverse
from article.models import *
from utils import myjson
from django.conf import settings
from django.views.decorators.http import require_http_methods
from forms import *
from utils.myemail import send_email
from qiniu import Auth,put_file
from django.core.cache import cache
from frontauth.models import FrontUserModel,FrontUser
from frontauth.utils import login,logout
from frontauth.decorators import front_login_required
from django.db.models import Q


@front_login_required
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

@front_login_required
@require_http_methods(['POST'])
def update_profile(request):
    
    # 1.更新头像
    # 2.更新用户名
    form = UpdateFrontProfileForm(request.POST)
    if form.is_valid():
        front_username = form.cleaned_data.get('front_username',None)
        portrait = form.cleaned_data.get('portrait',None)
        email = form.cleaned_data.get('email')
        print email
        user = FrontUserModel.objects.filter(email=email).first()
        if user:
            user.username = front_username
            user.portrait = portrait
            user.save()
        # # 获取FrontUserModel中所有用户信息
        # users = FrontUserModel.objects.all()  
        # user = users.filter(email="sun569589854@163.com").first()
        # frontUser = FrontUser.objects.filter(user__pk=user.pk).first()
        # 如果FrontUser表中已存在数据与user对应 直接更新
        # if frontUser:
            # frontUser.portrait = portrait
        # 否则，先新建一个frontuser模型 再保存
        # else:
            # frontUser = FrontUser(portrait=portrait,user=user)
        # frontUser.save()
        # return JsonResponse({'code':200})
        return myjson.json_result()
    else:
        print '------------------------fial'
        # return JsonResponse({'error':form.errors})
        return myjson.json_params_error(message=u'表单验证错误！')

def article_list(request,category_id=0,page=1):
    categoryId = int(category_id)
    currentPage = int(page)
    
    start = (currentPage-1)*settings.NUM_PAGE
    end = start + settings.NUM_PAGE

    categorys = CategoryModel.objects.all()
    articles = ArticleModel.objects.all()
    top_articles = None
    
    # 若url中存在id 则筛选出相应文章
    if categoryId>0:
        articles = articles.filter(category__pk=categoryId).order_by('public_date')
    else:
        top_articles = articles.filter(top__isnull=False).order_by('-top__Alter_time')
        articles = articles.filter(top__isnull=True).order_by('public_date')

    # 需要将其转化为数组
    articles = list(articles.values()[start:end])

    context = {
        'articles':articles,
        'c_page': currentPage
    }

    if request.is_ajax():
        return myjson.json_result(data=context)
    else:
        context['categorys'] = categorys
        context['c_category'] = CategoryModel.objects.filter(pk=categoryId).first()
        context['top_articles'] = top_articles

    return render(request,'front_article_list.html',context)



 
def article_detail(request,article_id=''):
    articleId = article_id
    if articleId:
        articleModel = ArticleModel.objects.filter(pk=articleId).first()
        if articleModel:
            comments = articleModel.commentmodel_set.all()
            context = {
                'articles':articleModel,
                'categorys':CategoryModel.objects.all(),
                'c_category':articleModel.category,
                'tags':articleModel.tags.all(),
                'comments':comments
            }
            return render(request,'front_article_detail.html',context)
        else:
            return myjson.json_params_error(message=u'该文章不存在！')
    else:
        return myjson.json_params_error(message=u'文章id不能为空！')


@require_http_methods(['GET','POST'])
def signup(request):
    if request.method == 'GET':
        #记住来源的url，如果没有则设置为首页('/')
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request,'front_signup.html')
    else:
        form = SignupForm(request.POST)
        refresh_url = request.session['login_from']
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # 给用户发送一封激活邮件
            cache_data = {
                'email':email,
                'username':username,
                'password':password
            }
            # 注册验证(检验邮箱 用户名是否已被注册)          
            is_email_exist = FrontUserModel.objects.filter(email=email).exists()   
            is_username_exist = FrontUserModel.objects.filter(username=username).exists()   
            # print is_username_exist,is_email_exist
            if is_email_exist:  
                return render(request,'front_signup.html',{'error':"该邮箱已被注册！"})  
            if is_username_exist:  
                return render(request,'front_signup.html',{'error':"账号已存在！"}) 
            elif send_email(request,email,'front_check_email',subject='注册验证',cache_data=cache_data,message=u' 进行登录，工作人员不会向您索取验证码，请勿泄露。消息来自：Mack的博客',signup=True):
                # 成功登录后返回原来页面
                # return HttpResponseRedirect(request.session['login_from'])
                return render(request,'front_aftersignup.html',{'refresh_url':refresh_url})
            else:
                return HttpResponse(u'邮件发送失败！')
        else:
            return render(request,'front_signup.html',{'error':form.get_error()})

def check_email(request,code=''):
    cache_data = cache.get(code)
    email = cache_data.get('email')
    username = cache_data.get('username')
    password = cache_data.get('password')

    user = FrontUserModel(email=email,username=username,password=password)
    user.save()

    # return HttpResponse(u'注册成功！')
    return redirect(reverse('front_signin'))



@require_http_methods(['GET','POST'])
def signin(request):
    if request.method == 'GET':
        #记住来源的url，如果没有则设置为首页('/')
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request,'front_signin.html')
    else:
        form = SigninForm(request.POST)
        refresh_url = request.session['login_from']
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = login(request,email,password)
            if user:
                remember = form.cleaned_data.get('remember')
                # 是否记住我
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)

                # 成功登录后返回原来页面
                return render(request,'front_afterlogin.html',{'refresh_url':refresh_url})
            else:
                return render(request,'front_signin.html',{'error':u'用户名或密码错误！'})

        else:
            return render(request,'front_signin.html',{'error':form.get_error()})

def signout(request):
    logout(request)
    # 退出登录后返回原页面 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_http_methods(['GET','POST'])
def forget_password(request):
    if request.method == 'GET':
        return render(request,'front_forgetpwd.html')
    else:
        form = ForgetpwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = FrontUserModel.objects.filter(email=email).first()
            if user:
                if send_email(request,email,'front_reset_password',subject='密码重置',message=u' 进行重置密码,请在10分钟内完成验证，工作人员不会向您索取验证码，请勿泄露。消息来自：Mack的博客'):
                    return HttpResponse(u'邮件发送成功！')
                else:
                    return HttpResponse(u'邮件发送失败！')
            else:
                return render(request,'front_forgetpwd.html',{'error':u'该用户不存在!'})
        else:
            return render(request,'front_forgetpwd.html',{'error':form.get_error()})

def reset_password(request,code=''):
    if request.method == 'GET':
        return render(request,'front_resetpwd.html')
    else:
        form = ResetpwdForm(request.POST)
        if form.is_valid():
            # 需要从缓存中通过code获取email
            email = cache.get(code)
            password = form.cleaned_data.get('password')
            user = FrontUserModel.objects.filter(email=email).first()
            if user:
                user.update_password(password)
                return HttpResponse(u'密码修改成功！')
            else:
                return HttpResponse(u'没有该用户！')    
        else:
            return render(request,'front_resetpwd.html',{'error':form.get_error()})

# 评论
@require_http_methods(['POST'])
@front_login_required
def comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        articleId = form.cleaned_data.get('article_id')
        articleModel = ArticleModel.objects.filter(pk=articleId).first()
        if articleModel:
            commentModel = CommentModel(content=content,article=articleModel,author=request.front_user)
            commentModel.save()
            return redirect(reverse('front_article_detail',kwargs={'article_id':articleId}))
        else:
            return myjson.json_params_error(message=u'该文章不存在！')
    else:
        return myjson.json_params_error(message=form.get_error())

@require_http_methods(['GET'])
def cms_search(request):
    # 从前端页面获取name为query的元素
    q = request.GET.get('query')
    if q:
        # icontains不区分大小写
        articls = ArticleModel.objects.filter(Q(title__icontains=q)|Q(content_html__icontains=q))
        context = {
            'articles':articls,
            'categorys':CategoryModel.objects.all()
        }
        return render(request,'front_search.html',context)
    else:
        return myjson.json_params_error(message=u'请输入查询内容！')


def front_settings(request):
    # 1.修改用户名
    # 2.修改头像
    # 3.修改邮箱
    return render(request,'front_settings.html')
