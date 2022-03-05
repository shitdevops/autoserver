from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse, reverse, get_object_or_404
from .models import User, LoginLog, Group
from .forms import LoginForm, ChangePasswordForm
from django.http import JsonResponse
import time, datetime
from .tool import login_required, admin_required
from server.models import *
import json
# Create your views here.


def login_event_log(user, event_type, detail, address, useragent):
    event = LoginLog()
    event.user = user
    event.event_type = event_type
    event.detail = detail
    event.address = address
    event.useragent = useragent
    event.save()


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect(reverse('assets:dashboard'))
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        error_message = '请检查填写的内容!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            print(username)
            print(password)
            try:
                user = User.objects.get(username=username)
                if not user.enabled:
                    error_message = '用户已禁用!'
                    login_event_log(user, 3, '用户 {} 已禁用'.format(username), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
                    return render(request, 'login/login.html', locals())
            except BaseException:
                error_message = '用户不存在!'
                login_event_log(None, 3, '用户 {} 不存在'.format(username), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
                return render(request, 'login/login.html', locals())
            if user.password == password:
                request.session.set_expiry(0)
                request.session['is_superuser'] = False
                if user.role == 1:  # 超管
                    request.session['is_superuser'] = True
                    print(request.session['is_superuser'])
                request.session['is_login'] = True
                request.session['userid'] = user.id
                request.session['username'] = user.username
                request.session['nickname'] = user.nickname
                now = int(time.time())
                request.session['logintime'] = now
                request.session['lasttime'] = now
                login_event_log(user, 1, '用户 {} 登陆成功'.format(username), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
                return redirect(reverse('assets:dashboard'))
            else:
                error_message = '密码错误!'
                login_event_log(user, 3, '用户 {} 密码错误'.format(username), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
                return render(request, 'login/login.html', locals())
        else:
            login_event_log(None, 3, '登陆表单验证错误', request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return render(request, 'login/login.html', locals())
    return render(request, 'login/login.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('user:login'))
    else:
        try:
            user = User.objects.get(id=int(request.session.get('userid')))
            request.session.flush()  # 清除所有后包括django-admin登陆状态也会被清除
            login_event_log(user, 2, '用户 {} 退出'.format(user.username), request.META.get('REMOTE_ADDR', None),
                            request.META.get('HTTP_USER_AGENT', None))
        except Exception:
            request.session.clear()  # 防止 session获取到已经删除的用户ID报错 清空session
            return redirect(reverse('user:login'))
    return redirect(reverse('user:login'))


@login_required
def user_info(request):
    user = get_object_or_404(User, pk=request.session.get('userid'))
    return render(request, 'login/user_info.html', locals())


@login_required
def profile_edit(request):
    user = get_object_or_404(User, pk=request.session.get('userid'))
    return render(request, 'login/profile_edit.html', locals())


@login_required
def change_passwd(request):
    changepasswd_form = ChangePasswordForm(request.POST)
    if changepasswd_form.is_valid():
        username = request.session.get('username')
        oldpassword = changepasswd_form.cleaned_data.get('oldpasswd')
        newpasswd = changepasswd_form.cleaned_data.get('newpasswd')
        newpasswdagain = changepasswd_form.cleaned_data.get('newpasswdagain')
        print(username, oldpassword, newpasswd, newpasswdagain)
        try:
            user = User.objects.get(username=username)
            if not user.enabled:
                error_message = '用户已禁用!'
                login_event_log(user, 4, '用户 {} 已禁用'.format(username), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
                return JsonResponse({"code": 401, "err": error_message})
            if newpasswd != newpasswdagain:
                error_message = '两次输入的新密码不一致'
                login_event_log(user, 4, '两次输入的新密码不一致', request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
                return JsonResponse({"code": 400, "err": error_message})
        except BaseException:
            error_message = '用户不存在!'
            login_event_log(None, 4, '用户 {} 不存在'.format(username), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({"code": 403, "err": error_message})
        if user.password == oldpassword:
            data = {'password': newpasswd}
            User.objects.filter(username=username).update(**data)
            login_event_log(user, 5, '用户 {} 修改密码成功'.format(username), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({"code": 200, "err": ""})
        else:
            error_message = '当前密码错误!'
            login_event_log(user, 4, '用户 {} 当前密码错误'.format(username), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({"code": 404, "err": error_message})
    else:
        username = request.session.get('username')
        error_message = '请检查填写的内容!'
        user = User.objects.get(username=username)
        login_event_log(user, 4, '修改密码表单验证错误', request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
        return JsonResponse({"code": 406, "err": error_message})


@admin_required
@login_required
def audit_login(reqeust):
    events = LoginLog.objects.all()
    return render(reqeust, 'login/audit_login.html', locals())


@admin_required
@login_required
def user_lists(request):
    users = User.objects.exclude(pk=request.session['userid'])  # exclude 排除当前登录用户
    return render(request, 'login/user_lists.html', locals())



@admin_required
@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    hosts_count = RemoteUserBindHost.objects.filter(Q(user__id=user_id)).distinct().count()
    return render(request, 'login/user_detail.html', locals())


@admin_required
@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    other_groups = Group.objects.filter(    # 查询当前用户不属于的组
        ~Q(user__id=user_id),
    )
    other_hosts = RemoteUserBindHost.objects.filter(
        ~Q(user__id=user_id),
    )
    sex_choices = (
        ('male', "男"),
        ('female', "女"),
    )
    role_choices = (
        (2, '普通用户'),
        (1, '超级管理员'),
    )
    return render(request, 'login/user_edit.html', locals())


@login_required
@admin_required
def user_add(request):
    all_groups = Group.objects.all()
    all_hosts = RemoteUserBindHost.objects.all()
    sex_choices = (
        ('male', '男'),
        ('female', '女'),
    )
    role_choices = (
        (2, '普通用户'),
        (1, '超级管理员'),
    )
    return render(request, 'login/user_add.html', locals())


@admin_required
@login_required
def group_lists(request):
    groups = Group.objects.all()
    return render(request, 'login/group_lists.html', locals())


@admin_required
@login_required
def group_add(request):
    all_users = User.objects.exclude(pk=request.session['userid'])
    all_hosts = RemoteUserBindHost.objects.all()
    return render(request, 'login/group_add.html', locals())


@admin_required
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    return render(request, 'login/group_detail.html', locals())


@login_required
@admin_required
def group_edit(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    other_users = User.objects.filter(    # 查询当前组不包含的用户
        ~Q(groups__id=group_id),
        ~Q(id=request.session['userid']),
    )
    other_hosts = RemoteUserBindHost.objects.filter(
        ~Q(group__id=group_id),
    )
    return render(request, 'login/group_edit.html', locals())




