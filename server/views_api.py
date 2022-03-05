# _*_ coding:utf-8 _*_
# By:赵先宇
import traceback

import requests
from django.db.models import Q
from django.shortcuts import get_object_or_404
from user.tool import login_required, admin_required
from .forms import *
from user.models import User, RemoteUserBindHost, LoginLog
from django.http import JsonResponse
from .models import RemoteUser
from .models import HostGroup


def login_event_log(user, event_type, detail, address, useragent):
    event = LoginLog()
    event.user = user
    event.event_type = event_type
    event.detail = detail
    event.address = address
    event.useragent = useragent
    event.save()


@login_required
@admin_required
def host_add(request):
    addhost_form = AddHostForm(request.POST)
    if addhost_form.is_valid():
        log_user = request.session.get('username')
        hostname = addhost_form.cleaned_data.get('hostname')
        int_ip = addhost_form.cleaned_data.get('int_ip')
        #ex_ip = addhost_form.cleaned_data.get('ex_ip')
        env = addhost_form.cleaned_data.get('env')
        port = addhost_form.cleaned_data.get('port')
        release = addhost_form.cleaned_data.get('release')
        memo = addhost_form.cleaned_data.get('memo')
        enabled = addhost_form.cleaned_data.get('enabled')
        binduserid = addhost_form.cleaned_data.get('binduserid')
        data = {
            'hostname': hostname,
            'int_ip': int_ip,
            #'ex_ip': ex_ip,
            'env': env,
            'port': port,
            'release': release,
            'memo': memo,
            'enabled': enabled,
        }
        try:
            user = User.objects.get(username=log_user)
            remoteuser = RemoteUser.objects.get(id=binduserid)
            data['remote_user'] = remoteuser
            remoteuserbindhost = RemoteUserBindHost.objects.create(**data)
            login_event_log(user, 12, '主机 [{}] 添加成功'.format(remoteuserbindhost.hostname),
                            request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({"code": 200, "err": ""})
        except:
            print(traceback.format_exc())
            error_message = '未知错误!'
            return JsonResponse({"code": 400, "err": error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({"code": 401, "err": error_message})


@login_required
def host_update(request):
    changehost_form = ChangeHostForm(request.POST)
    if changehost_form.is_valid():
        log_user = request.session.get('username')
        hostid = changehost_form.cleaned_data.get('hostid')
        int_ip = changehost_form.cleaned_data.get('int_ip')
        #ex_ip = changehost_form.cleaned_data.get('ex_ip')
        env = changehost_form.cleaned_data.get('env')
        port = changehost_form.cleaned_data.get('port')
        release = changehost_form.cleaned_data.get('release')
        memo = changehost_form.cleaned_data.get('memo')
        enabled = changehost_form.cleaned_data.get('enabled')
        binduserid = changehost_form.cleaned_data.get('binduserid')
        data = {
            'int_ip': int_ip,
            #'ex_ip': ex_ip,
            'env': env,
            'port': port,
            'release': release,
            'memo': memo,
            'enabled': enabled,
        }
        try:
            user = User.objects.get(username=log_user)
            remoteuser = RemoteUser.objects.get(id=hostid)
            data['remote_user'] = remoteuser
            RemoteUserBindHost.objects.filter(id=hostid).update(**data)
            login_event_log(user, 14, '主机 [{}] 更新成功'.format(RemoteUserBindHost.objects.get(id=hostid).hostname),
                            request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({'code': 200, "err": ""})
        except:
            error_message = '未知错误!'
            return JsonResponse({"code": 400, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 401, 'err': error_message})


@login_required
def host_delete(request):
    pk = request.POST.get('id', None)
    log_user = User.objects.get(username=request.session.get("username"))
    if not pk:
        error_message = '不合法的请求参数!'
        return JsonResponse({'code': 400, 'err': error_message})
    host = get_object_or_404(RemoteUserBindHost, pk=pk)
    host.delete()
    login_event_log(log_user, 13, '主机 [{}] 删除成功'.format(host.hostname),
                    request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
    return JsonResponse({'code': 200, 'err': ""})


@login_required
@admin_required
def user_add(request):
    adduser_form = AddUserForm(request.POST)
    if adduser_form.is_valid():
        log_user = request.session.get('username')
        name = adduser_form.cleaned_data.get('name')
        username = adduser_form.cleaned_data.get('username')
        password = adduser_form.cleaned_data.get('password')
        memo = adduser_form.cleaned_data.get('memo')
        enabled = adduser_form.cleaned_data.get('enabled')
        superusername = adduser_form.cleaned_data.get('superusername', None)
        superpassword = adduser_form.cleaned_data.get('superpassword', None)
        if enabled:
            if not superusername or not superpassword:
                error_message = '超级用户或者超级密码不能为空!'
                return JsonResponse({"code": 400, "err": error_message})

        data = {
            'name': name,
            'username': username,
            'password': password,
            'memo': memo,
            'enabled': enabled,
            'superusername': superusername,
            'superpassword': superpassword,
        }
        try:
            if RemoteUser.objects.filter(name=name).count() > 0:
                error_message = '主机用户已存在'
                return JsonResponse({"code": 401, "err": error_message})
            user = User.objects.get(username=log_user)
            update_user = RemoteUser.objects.create(**data)
            login_event_log(user, 15, '主机用户 [{}] 添加成功'.format(update_user.name), request.META.get('REMOTE_ADDR', None),
                            request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({"code": 200, "err": ""})
        except:
            # print(traceback.format_exc())
            error_message = '未知错误!'
            return JsonResponse({"code": 402, "err": error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({"code": 403, "err": error_message})

@login_required
@admin_required
def user_update(request):
    changeuser_form = ChangeUserForm(request.POST)
    if changeuser_form.is_valid():
        log_user = request.session.get('username')
        userid = changeuser_form.cleaned_data.get('userid')
        username = changeuser_form.cleaned_data.get('username')
        password = changeuser_form.cleaned_data.get('password')
        memo = changeuser_form.cleaned_data.get('memo')
        enabled = changeuser_form.cleaned_data.get('enabled')
        superusername = changeuser_form.cleaned_data.get('superusername')
        superpassword = changeuser_form.cleaned_data.get('superpassword')
        if enabled:
            if not superusername or not superpassword:
                error_message = '超级用户或超级密码不能为空!'
                return JsonResponse({'code': 400, 'err': error_message})
        data = {
            'username': username,
            'password': password,
            'memo': memo,
            'enabled': enabled,
            'superusername': superusername,
            'superpassword': superpassword,
        }
        try:
            user = User.objects.get(username=log_user)
            RemoteUser.objects.filter(id=userid).update(**data)
            login_event_log(user, 17, '主机用户 [{}] 更新成功'.format(RemoteUser.objects.get(id=userid).name),
                            request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({'code': 200, 'err': ""})
        except:
            error_message = '主机用户不存在!'
            return JsonResponse({'code': 401, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 402, 'err': error_message})


@login_required
@admin_required
def user_delete(request):
    pk = request.POST.get('id', None)
    log_user = User.objects.get(username=request.session.get("username"))
    if not pk:
        error_message = '不合法的请求参数!'
        return JsonResponse({'code': 400, 'err': error_message})
    remoteuser = get_object_or_404(RemoteUser, pk=pk)
    if remoteuser.remoteuserbindhost_set.all().count() != 0:
        error_message = '用户已绑定主机!'
        return JsonResponse({'code': 401, 'err': error_message})
    remoteuser.delete()
    login_event_log(log_user, 16, '主机用户 [{}] 删除成功'.format(remoteuser.name),
                    request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
    return JsonResponse({'code': 200, 'err': ""})


@login_required
def host_group_delete(request):
    pk = request.POST.get('id', None)
    user = User.objects.get(id=int(request.session.get('userid')))
    if not pk:
        error_message = '不合法的请求参数!'
        return JsonResponse({'code': 400, 'err': error_message})
    group = get_object_or_404(HostGroup, pk=pk, user=user)
    group.delete()
    login_event_log(user, 28, '主机组 [{}] 删除成功'.format(group.group_name), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
    return JsonResponse({'code': 200, 'err': ""})


@login_required
def host_group_update(request):
    changegroup_form = ChangeGroupForm(request.POST)
    if changegroup_form.is_valid():
        log_user = request.session.get('username')
        groupid = changegroup_form.cleaned_data.get('groupid')
        memo = changegroup_form.cleaned_data.get('memo')
        hosts = changegroup_form.cleaned_data.get('hosts')
        if hosts:
            try:
                hosts = [int(host) for host in hosts.split(',')]
            except Exception:
                error_message = '请检查填写的内容!'
                return JsonResponse({'code': 401, 'err': error_message})
        else:
            hosts = None
        data = {
            'memo': memo,
        }
        try:
            user = User.objects.get(username=log_user)
            HostGroup.objects.filter(id=groupid, user=user).update(**data)
            update_group = HostGroup.objects.get(id=groupid, user=user)
            if hosts: # 更新主机多对多
                if request.session['is_superuser']:
                    update_hosts = RemoteUserBindHost.objects.filter(id__in=hosts)
                else:
                    update_hosts = RemoteUserBindHost.objects.filter(
                        Q(user__username=request.session['username']) | Q(group__user__username=request.session['username']),
                        Q(id__in=hosts),
                    )
                update_group.remoteuserbindhost_set.set(update_hosts)
            else:
                update_group.remoteuserbindhost_set.set.clear()
            update_group.save()
            login_event_log(user, 29, '主机组 [{}] 更新信息成功'.format(update_group.group_name), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({"code": 200, "err": ""})
        except Exception:
            error_message = '主机组不存在!'
            return JsonResponse({'code': 402, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 403, 'err': error_message})

@login_required
@admin_required
def host_group_add(request):
    addgroup_form = AddGroupForm(request.POST)
    if addgroup_form.is_valid():
        login_user = request.session.get('username')
        groupname = addgroup_form.cleaned_data.get('groupname')
        memo = addgroup_form.cleaned_data.get('memo')
        hosts = addgroup_form.cleaned_data.get('hosts')
        if hosts:
            try:
                hosts = [int(host) for host in hosts.split(',')]
            except Exception:
                error_message = '请检查填写的内容!'
                return JsonResponse({'code': 401, 'err': error_message})
        else:
            hosts = None
        data = {
            'group_name': groupname,
            'memo': memo,
        }
        try:
            user = User.objects.get(username=login_user)
            if HostGroup.objects.filter(group_name=groupname, user=user).count() > 0:
                error_message = '主机组已存在'
                return JsonResponse({'code': 402, 'err': error_message})
            data['user'] = user
            update_group = HostGroup.objects.create(**data)

            if hosts: # 更新多对多
                if request.session['is_superuser']:
                    update_hosts = RemoteUserBindHost.objects.filter(id__in=hosts)
                else:
                    update_hosts = RemoteUserBindHost.objects.filter(
                        Q(user__username=request.session['username']) | Q(group__user__username=request.session['username']),
                        Q(id__in=hosts),
                    )
                update_group.remoteuserbindhost_set.set(update_hosts)
            else:
                update_group.remoteuserbindhost_set.clear()
            update_group.save()
            login_event_log(user, 27, '主机组 [{}] 添加成功'.format(update_group.group_name), request.META.get('REMOTE_ADDR', None),
                      request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({"code": 200, "err": ""})
        except Exception:
            error_message = '主机组添加错误'
            return JsonResponse({'code': 403, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 404, 'err': error_message})
