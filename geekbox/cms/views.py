from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUser
from .forms import CreateStiker
from .forms import CreateComment,CreateReply

from django.contrib import messages

from geekbox.settings import INVITEDCODE

from .models.Comments import Comment,Reply
from .models.Stikers import Stiker,Topic
from .models.Users import StikerUser
from django.contrib.auth.models import User

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage

import django.utils.timezone as timezone

from django.views.decorators.csrf import csrf_exempt
# 贴文相关

# 检查邀请码
def is_right(InvitedCode):
        if InvitedCode in INVITEDCODE:
            return True

# 首页，贴文详细页,主题页
def index(request):
    user=request.user
    userage=None
    if user.id is None:              
        user=None
    else:
        user=StikerUser.objects.get(username=user.username)  # 这么操作会导致非注册系统创建的管理员账户无法登录主页，也好，
        user_age=timezone.now()-user.created_time    # 再做异常判断可能会引入逻辑漏洞，所以这块不改了
        userage=user_age.days           # time.delta对象

    # return HttpResponse('index of library')
    topics=Topic.objects.all()
    topics_hotest=topics[:4]
    topics_name_list=[i.name for i in topics]

    stikers=Stiker.objects.all().order_by("-last_update_time")
    Top3_comments=Comment.objects.all().order_by("-stars")[:3]
    # Top3_comments_informations=zip()
    # stikers_20=stikers.order_by("-id")[:20]     # 一页20条
    # 分页
    paginator=Paginator(stikers,20)
    if request.method=="GET":
        page=request.GET.get('page')
        try:
            stikers_each_page=paginator.page(page)
        except PageNotAnInteger:
            stikers_each_page = paginator.page(1)
        except InvalidPage:
            # 请求的页数不存在, 重定向页面
            return redirect('cms')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            stikers_each_page = paginator.page(paginator.num_pages)


    Top11_stikers=stikers.order_by("-stars")[:11]
    Top3_stikers=Top11_stikers[:3]
    Top4_7_stikers=Top11_stikers[3:7]
    Top8_11_stikers=Top11_stikers[7:11]

    replys=Reply.objects.all()
    Top3_replys=replys.order_by("-stars")[:3]
    # 对首页的stikers进行分页动态加载

    # 首页的创建功能删去,改成单独一页
    # 创建话题的表单
    # form=CreateStiker(initial={'author':[user.id,]})      写法不对 没有生效
    # form=CreateStiker()
    # if request.method == "POST":
    #     form=CreateStiker(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         title=form.cleaned_data.get('title')
    #         Stiker.objects.filter(title=title).update(author=user.id)
    #                         # 换别的表单创建方法也可以实现
    #         return redirect('cms')

    context={
        'user':user,
        'userage':userage,

        'topics':topics_hotest,           # stikerbar的topics，sidenav的topics，topicbar的反查
        'topics_name_list':topics_name_list,            # 考虑到sidenav的复用
        'stikers_each_page':stikers_each_page,        # 分页stikers
        'page_range':paginator.page_range,
        
        'Top3_stikers':Top3_stikers,            # carousel的Top3
        'Top4_7_stikers':Top4_7_stikers,      # sikerbar的热议话题 8条
        'Top8_11_stikers':Top8_11_stikers,

        'Top3_comments':Top3_comments,          # carousel的Top3
        'Top3_replys':Top3_replys,              # carousel的Top3

        # 'form':form,                        # 话题创建表单
    
    }
    return render(request,'cms/index.html',context)

def detail(request,cms_id=None):
    if cms_id==None:
        return redirect(reverse(index))

    stiker=Stiker.objects.get(id=cms_id)
    comments_list=stiker.stiker_comments_set.all()


    user=request.user
    userage=None
    if user.id is None:              
        user=None
    else:
        user=StikerUser.objects.get(username=user.username)  # 这么操作会导致非注册系统创建的管理员账户无法登录主页，也好，
        user_age=timezone.now()-user.created_time    # 再做异常判断可能会引入逻辑漏洞，所以这块不改了
        userage=user_age.days 

    topics=Topic.objects.all()
    topics_name_list=[i.name for i in topics]

    context={
        'stiker':stiker,
        'comments_list':comments_list,
        # 'replys_set':replys_set,

        'user':user,
        'userage':userage,

        'topics_name_list':topics_name_list,

    }


    return render(request,'cms/detail.html',context)

# 话题主页
def topicPage(request,topic_name=None):
    if topic_name==None:
        return redirect('cms')
    
    user=request.user
    userage=None
    if user.id is None:              
        user=None
    else:
        user=StikerUser.objects.get(username=user.username)  # 这么操作会导致非注册系统创建的管理员账户无法登录主页，也好，
        user_age=timezone.now()-user.created_time    # 再做异常判断可能会引入逻辑漏洞，所以这块不改了
        userage=user_age.days 

    topics=Topic.objects.all()
    topics_name_list=[i.name for i in topics]

    try:
        topic=topics.get(name=topic_name)
        help_text=topic.help_text
        stikers=topic.topic_stikers_set.all().order_by('-last_update_time')
    except:
        return redirect('cms')

    paginator=Paginator(stikers,20)
    if request.method=="GET":
        page=request.GET.get('page')
        try:
            stikers_each_page=paginator.page(page)
        except PageNotAnInteger:
            stikers_each_page = paginator.page(1)
        except InvalidPage:
            # 请求的页数不存在, 重定向页面
            return redirect('cms')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            stikers_each_page = paginator.page(paginator.num_pages)



    context={
        'user':user,
        'userage':userage,
        
        'topic_name':topic_name,
        'help_text':help_text,
                                # 复用首页的组件
        'topics_name_list':topics_name_list,

        'stikers_each_page':stikers_each_page,
        }
    return render(request,'cms/topic.html',context)

# 用户主页，修改个人信息
def userPage(request,username=None):
    if username:
        user=StikerUser.objects.get(username=username)

        context={
            'user':user,
        }
        return render(request,'cms/userpage.html',context)
    return redirect('cms')

def update_user(request,user_id=None):
    if user_id:
        user=StikerUser.objects.get(id=user_id)
        if user.id == request.user.id:
            if request.method=="POST":
                user_form=CreateUser(instance=user,data=request.POST)
                if user_form.is_valid():
                    # 改用户名的情况
                    user_form.save()
                    messages.success(request,"修改成功！请重新登录！")
                    return render(request,'cms/messages.html')
            elif request.method=="GET":
                update_form=CreateUser(instance=user)
                context={
                    'update_form':update_form,
                }
                return render(request,'cms/update_userinfo.html',context)
            return redirect('cms')
        else:
            return redirect('cms')
    return redirect('cms')

## 两个功能
# 评论，回复分开写，赋予的能力一样
# 创建评论
@login_required(login_url='/login')
def post_comment(request,stiker_id):
    if request.method == "POST":                    # 这块直接前端负责post
        stiker = get_object_or_404(Stiker,id=stiker_id)
        comment_form=CreateComment(request.POST)
        if comment_form.is_valid:
            try:
                create_comment=comment_form.save(commit=False)
                create_comment.stiker=stiker
                create_comment.author=StikerUser.objects.get(username=request.user)
                create_comment.save()
                comment_form.save_m2m()
                messages.success(request,"评论成功！刷新页面后可以再次评论！")
                return render(request,'cms/messages.html')
            except:
                messages.warning(request,"评论失败！刷新页面可重新评论！")
                return render(request,'cms/messages.html')
    elif request.method=="GET":
        comment_form=CreateComment()
        context={
            'create_comment_form':comment_form,
        }
        return render(request,'cms/comment.html',context)
    else:
        return redirect('detail',stiker_id)

# 修改评论
@login_required(login_url='/login')
def update_comment(request,comment_id):
    if comment_id:
        comment=get_object_or_404(Comment,id=comment_id)
        if comment.author.username == request.user.username:            # 用户名是唯一的 可以用用户名判断
            if request.method=="POST":
                comment_form=CreateComment(instance=comment,data=request.POST)
                if comment_form.is_valid():
                    try:
                        comment_form.save()                            # 作者自己改成别人post的情况 X ,, 表单只有 修改comment的字段
                        messages.success(request,"修改成功！请关闭弹窗刷新页面")
                        return render(request,'cms/messages.html')
                    except:
                        messages.warning(request,"数据有误，修改失败！")
                        return render(request,'cms/messages.html')
                else:
                    messages.warning(request,"数据有误，修改失败！")
                    return render(request,'cms/messages.html')
            else:
                # stiker_form=CreateStiker(initial={"title":stiker.title,'stiker':stiker.stiker})
                update_comment_form=CreateComment(instance=comment)
                context={
                    'update_comment_form': update_comment_form,
                }
                return render(request,'cms/update_comment.html',context)
        else:
            return redirect('detail',comment.stiker.id)
    else:
        return redirect('detail',comment.stiker.id)

# 删除评论
@login_required(login_url='/login')
def delete_comment(request,comment_id):
    if comment_id is None:
        return redirect("cms")
    else:
        comment=Comment.objects.get(id=comment_id)
        if comment.author.id == request.user.id:
            delete=comment.delete()
            return redirect('detail',comment.stiker.id)
        else:
            return redirect('detail',comment.stiker.id)


# 创建回复
@login_required(login_url='/login')
def post_reply(request,comment_id,parent_id=None):
    if request.method=="POST":
        comment=get_object_or_404(Comment,id=comment_id)
        reply_form=CreateReply(request.POST)
        if reply_form.is_valid:
            try:
                create_reply=reply_form.save(commit=False)
                create_reply.comment=comment
                create_reply.author=StikerUser.objects.get(username=request.user)
                # 一层评论的 parent是null
                if parent_id:
                    parent_reply=Reply.objects.get(id=parent_id)
                    create_reply.parent=parent_reply
                    create_reply.save()
                    reply_form.save_m2m()
                    messages.success(request,"回复成功！刷新页面后可以再次回复！")
                    return render(request,'cms/messages.html')
                create_reply.save()
                reply_form.save_m2m()
                messages.success(request,"回复成功！刷新页面后可以再次回复！")
                return render(request,'cms/messages.html')
            except:
                messages.success(request,"回复无效！刷新页面后可以重新回复！")
                return render(request,'cms/messages.html')
        else:
            messages.success(request,"回复无效！刷新页面后可以重新回复！")
            return render(request,'cms/messages.html')
    elif request.method == "GET":
        reply_form=CreateReply()
        context={
            'create_reply_form':reply_form,
        }
        return render(request,'cms/reply.html',context)
    else:
        return redirect('detail',comment.stiker.id)

# 修改回复
@login_required(login_url='/login')
def update_reply(request,reply_id):
    if reply_id:
        reply=get_object_or_404(Reply,id=reply_id)
        if reply.author.username == request.user.username:            # 用户名是唯一的 可以用用户名判断
            if request.method=="POST":
                reply_form=CreateReply(instance=reply,data=request.POST)
                if reply_form.is_valid():
                    try:
                        reply_form.save()                            # 作者自己改成别人post的情况 X ,, 表单只有 修改comment的字段
                        messages.success(request,"修改成功！请关闭弹窗刷新页面")
                        return render(request,'cms/messages.html')
                    except:
                        messages.warning(request,"数据有误，修改失败！")
                        return render(request,'cms/messages.html')
                else:
                    messages.warning(request,"数据有误，修改失败！")
                    return render(request,'cms/messages.html')
            else:
                # stiker_form=CreateStiker(initial={"title":stiker.title,'stiker':stiker.stiker})
                update_reply_form=CreateReply(instance=reply)
                context={
                    'update_reply_form': update_reply_form,
                    'reply':reply,
                }
                return render(request,'cms/update_reply.html',context)
        else:
            return redirect('detail',reply.comment.stiker.id)
    else:
        return redirect('detail',reply.comment.stiker.id)

# 删除回复
@login_required(login_url='/login')
def delete_reply(request,reply_id):
    if reply_id is None:
        return redirect("cms")
    else:
        reply=Reply.objects.get(id=reply_id)
        if reply.author.id == request.user.id:
            delete=reply.delete()
            return redirect('detail',reply.comment.stiker.id)
        else:
            return redirect('detail',reply.comment.stiker.id)


# 创建文章
@login_required(login_url='/login')
def create_stiker(request):
    create_stiker_form=CreateStiker()
    if request.method=="POST":
        create_stiker_form=CreateStiker(request.POST)
        if create_stiker_form.is_valid:
            create_stiker=create_stiker_form.save(commit=False)             # commit=F  不保存到数据库
            create_stiker.author=StikerUser.objects.get(username=request.user)
            if create_stiker.title:
                create_stiker.save()
                create_stiker_form.save_m2m()                           # 前面只会保存基本字段信息，多对多的信息需要再对原表单进行一次关联保存
                return redirect('cms')
            else:
                messages.warning(request,'标题不能为空,贴文创建失败！')
                return render(request,'cms/messages.html')
        else:
            messages.warning(request,'数据输入有误,贴文创建失败！')
            return render(request,'cms/messages.html')


    context={
        'create_stiker_form':create_stiker_form,
    }

    return render(request,'cms/create_stiker.html',context)

# 修改文章
@login_required(login_url='/login')
def update_stiker(request,stiker_id=None):  
    if stiker_id:
        stiker=get_object_or_404(Stiker,id=stiker_id)
        if stiker.author.username == request.user.username:            # 用户名是唯一的 可以用用户名判断

            if request.method=="POST":
                stiker_form=CreateStiker(instance=stiker,data=request.POST)
                if stiker_form.is_valid():
                    save_form=stiker_form.save(commit=False)
                    # save_form.author=stiker.author                   # 防止改数据改到别人名下的可能性，多此一举，前端表单根本没有这个字段
                    save_form.last_update_time=timezone.now()
                    save_form.save()
                    stiker_form.save_m2m()
                    messages.success(request,"修改成功！请关闭弹窗刷新页面")
                    return render(request,'cms/messages.html')
                else:
                    messages.warning(request,"表单提交错误，修改失败！")
                    return render(request,'cms/messages.html')
            else:
                # stiker_form=CreateStiker(initial={"title":stiker.title,'stiker':stiker.stiker})
                stiker_form=CreateStiker(instance=stiker)           # 收到表单字段限制，传到前端的只有 标题 话题 内容的字段
                context={   
                    'stiker_form':stiker_form,
                }
                return render(request,'cms/update_stiker.html',context)

        else:
            return redirect('cms')
    else:
        return redirect('cms')


# 删除文章
@login_required(login_url='/login')
def delete_stiker(request,stiker_id=None): 
    if stiker_id is None:
        return redirect("cms")
    else:
        stiker=Stiker.objects.get(id=stiker_id)
        if stiker.author.id == request.user.id:
            delete=stiker.delete()
        return redirect('cms')


@login_required(login_url='/login')
@csrf_exempt
def star(request,type,id):
    if id:
        if request.method=="POST":
            if type == 'stiker':
                obj=get_object_or_404(Stiker,id=id)
            elif type == 'comment':
                obj=get_object_or_404(Comment,id=id)
            elif type == 'reply':
                obj=get_object_or_404(Reply,id=id)    
            else:
                return redirect('cms')
            obj.stars+=1
            obj.save()
            return HttpResponse('200')
        else:
            return HttpResponse('500')
    else:
        return redirect('cms')

@login_required(login_url='/login')
@csrf_exempt
def unstar(request,type,id):
    if id:
        if request.method=="POST":
            if type == 'stiker':
                obj=get_object_or_404(Stiker,id=id)
            elif type == 'comment':
                obj=get_object_or_404(Comment,id=id)
            elif type == 'reply':
                obj=get_object_or_404(Reply,id=id)    
            else:
                return redirect('cms')
            obj.unstars+=1
            obj.save()
            return HttpResponse('200')
        else:
            return HttpResponse('500')
    else:
        return redirect('cms')


# 登录注册登出
def loginPage(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('userpage',username)
        else:
            messages.info(request,"用户名或者密码错误")

    context={}        
    return render(request,'cms/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('cms')

def registerPage(request):
    form = CreateUser()
    # form =UserCreationForm()
    if request.method == "POST":
        form=CreateUser(request.POST)
        if not is_right(form['InvitedCode'].value()):
            return render(request,'cms/InvitedCodefailed.html')
        else:            
            if form.is_valid():
                form.save()
                messages.success(request,'用户 '+form.cleaned_data.get('username') + ' 注册成功')
                return redirect('login')
            else:
                pass

    context={'form':form}

    return render(request,'cms/register.html',context)
