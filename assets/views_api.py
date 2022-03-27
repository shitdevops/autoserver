import traceback

from django.shortcuts import render
from user.tool import login_required, admin_required
from .forms import *
from django.http import JsonResponse
from repository import models
from user.models import User
from user.models import LoginLog
from django.shortcuts import get_object_or_404, render


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
def business_update(request):
    changebus_form = ChangeBusinessForm(request.POST)
    if changebus_form.is_valid():
        log_user = request.session.get('username')
        busid = changebus_form.cleaned_data.get('busid')
        name = changebus_form.cleaned_data.get('name')
        memo = changebus_form.cleaned_data.get('memo')
        print(busid, name, memo)
        try:
            user = User.objects.get(username=log_user)
            models.BusinessUnit.objects.filter(pk=busid).update(name=name, memo=memo)
            login_event_log(user, 20, '业务线 {} 更新信息成功'.format(models.BusinessUnit.objects.get(pk=busid)), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({'code': 200, 'err': ""})
        except:
            error_message = '业务线不存在!'
            return JsonResponse({'code': 401, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 404, 'err': error_message})


@login_required
@admin_required
def business_delete(request):
    pk = request.POST.get('id', None)
    log_user = User.objects.get(username=request.session.get('username'))
    if not pk:
        error_message = '不合法的请求参数!'
        return JsonResponse({'code': 401, 'err': error_message})
    bus = get_object_or_404(models.BusinessUnit, pk=pk)
    if bus.server_set.all().count() != 0:
        error_message = '业务线下已有资产!'
        return JsonResponse({'code': 402, 'err': error_message})
    bus.delete()
    login_event_log(log_user, 19, '业务线 {} 删除成功'.format(bus.name), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
    return JsonResponse({'code': 200, 'err': ""})


@login_required
@admin_required
def business_add(request):
    addbus_form = AddBusinessForm(request.POST)
    if addbus_form.is_valid():
        log_user = request.session.get('username')
        name = addbus_form.cleaned_data.get('name')
        memo = addbus_form.cleaned_data.get('memo')
        try:
            if models.BusinessUnit.objects.filter(name=name).count() > 0:
                error_messge = '业务线名称不能重名'
                return JsonResponse({'code': 401, 'err': error_messge})
            user = User.objects.get(username=log_user)
            models.BusinessUnit.objects.create(name=name, memo=memo)
            login_event_log(user, 18, '业务线 {} 添加成功'.format(name), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({'code': 200, 'err': ""})
        except:
            error_messge = '未知错误!'
            return JsonResponse({'code': 401, 'err': error_messge})
    else:
        error_messge = '请检查填写的内容!'
        return JsonResponse({'code': 402, 'err': error_messge})


@login_required
@admin_required
def idc_add(request):
    addidc_form = AddIdcForm(request.POST)
    if addidc_form.is_valid():
        log_user = request.session.get('username')
        name = addidc_form.cleaned_data.get('name')
        memo = addidc_form.cleaned_data.get('memo')
        try:
            if models.IDC.objects.filter(name=name).count() > 0:
                error_message = '机房名称不能重复!'
                return JsonResponse({'code': 401, 'err': error_message})
            user = User.objects.get(username=log_user)
            models.IDC.objects.create(name=name, memo=memo)
            login_event_log(user, 21, '机房 {} 添加成功'.format(name), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({'code': 200, 'err': ""})
        except:
            error_message = '未知错误!'
            return JsonResponse({'code': 402, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 403, 'err': error_message})


@login_required
@admin_required
def idc_update(request):
    changeidc_form = ChangeIdcForm(request.POST)
    if changeidc_form.is_valid():
        log_user = request.session.get('username')
        idc_id = changeidc_form.cleaned_data.get('idc_id')
        name = changeidc_form.cleaned_data.get('name')
        memo = changeidc_form.cleaned_data.get('memo')
        print(idc_id, name, memo)
        try:
            user = User.objects.get(username=log_user)
            models.IDC.objects.filter(pk=idc_id).update(name=name, memo=memo)

            login_event_log(user, 23, '机房 {} 更新信息成功'.format(models.IDC.objects.get(pk=idc_id)), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({'code': 200, 'err': ""})
        except:
            error_message = '机房不存在!'
            return JsonResponse({'code': 401, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 404, 'err': error_message})


@login_required
@admin_required
def idc_delete(request):
    pk = request.POST.get('id', None)
    log_user = User.objects.get(username=request.session.get('username'))
    if not pk:
        error_message = '不合法的请求参数!'
        return JsonResponse({'code': 400, 'err': error_message})
    idc = get_object_or_404(models.IDC, pk=pk)
    if idc.server_set.all().count() != 0:
        error_message = '机房下已有资产!'
        return JsonResponse({'code': 401, 'err': error_message})
    idc.delete()
    login_event_log(log_user, 22, '机房 {} 删除成功'.format(idc.name), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
    return JsonResponse({'code': 200, 'err': ""})


@login_required
@admin_required
def server_update(request):
    changeasset_form = ChangeAssetForm(request.POST)
    if changeasset_form.is_valid():
        log_user = request.session.get('username')
        asset_id = changeasset_form.cleaned_data.get('asset_id')
        created = changeasset_form.cleaned_data.get('created')
        status = changeasset_form.cleaned_data.get('status')
        memo = changeasset_form.cleaned_data.get('memo')
        business_id = changeasset_form.cleaned_data.get('business_id')
        idc_id = changeasset_form.cleaned_data.get('idc_id')

        data = {
            'status': status,
            'created_by': created,
            'memo': memo,
        }

        try:
            user = User.objects.get(username=log_user)
            bus = models.BusinessUnit.objects.get(id=business_id)
            data['business_unit'] = bus
            i = models.IDC.objects.get(id=idc_id)
            data['idc'] = i
            models.Server.objects.filter(id=asset_id).update(**data)
            update_server = models.Server.objects.get(id=asset_id)

            update_server.save()
            login_event_log(user, 26, '资产 {} 更新信息成功'.format(models.Server.objects.get(id=asset_id).hostname),
                            request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({'code': 200, 'err': ""})
        except:
            print(traceback.format_exc())
            error_message = '未知错误!'
            return JsonResponse({'code': 402, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 403, 'err': error_message})


@login_required
@admin_required
def server_add(request):
    print(request.POST)
    addasset_form = AddAssetForm(request.POST)
    if addasset_form.is_valid():
        log_user = request.session.get('username')
        status = addasset_form.cleaned_data.get('status')
        created = addasset_form.cleaned_data.get('created')
        memo = addasset_form.cleaned_data.get('memo')
        hostname = addasset_form.cleaned_data.get('hostname')
        os_platform = addasset_form.cleaned_data.get('os_platform')
        os_version = addasset_form.cleaned_data.get('os_version')
        sn = addasset_form.cleaned_data.get('sn')
        manufacturer = addasset_form.cleaned_data.get('manufacturer')
        model = addasset_form.cleaned_data.get('model')
        cpu_count = addasset_form.cleaned_data.get('cpu_count')
        cpu_physical_count = addasset_form.cleaned_data.get('cpu_physical_count')
        cpu_model = addasset_form.cleaned_data.get('cpu_model')
        tags = addasset_form.cleaned_data.get('tag')
        idc_id = addasset_form.cleaned_data.get('idc_id')
        business_id = addasset_form.cleaned_data.get('business_id')


        data = {
            'hostname': hostname,
            'status': status,
            'created_by': created,
            'os_platform': os_platform,
            'memo': memo,
            'os_version': os_version,
            'sn': sn,
            'manufacturer': manufacturer,
            'model': model,
            'cpu_count': cpu_count,
            'cpu_physical_count': cpu_physical_count,
            'cpu_model': cpu_model,
        }
        try:
            if models.Server.objects.filter(hostname=hostname).count() > 0:
                error_message = '主机名已存在!'
                return JsonResponse({'code': 402, 'err': error_message})
            user = User.objects.get(username=log_user)
            bus = models.BusinessUnit.objects.get(id=business_id)
            data['business_unit'] = bus
            idc = models.IDC.objects.get(id=idc_id)
            data['idc'] = idc
            update_asset = models.Server.objects.create(**data)
            #
            # if tags:  # 更新多对多
            #     update_tags = models.Tag.objects.filter(id__in=tags)
            #     update_asset.tags.set(update_tags)
            # else:
            #     update_asset.tags.clear()
            # update_asset.save()

            login_event_log(user, 24, '资产 {} 添加成功'.format(update_asset.hostname), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
            return JsonResponse({'code': 200, 'err': ""})
        except:
            print(traceback.format_exc())
            error_message = '未知错误!'
            return JsonResponse({'code': 400, 'err': error_message})
    else:
        error_message = '请检查填写的内容!'
        return JsonResponse({'code': 401, 'err': error_message })


@login_required
@admin_required
def server_delete(request):
    pk = request.POST.get('id', None)
    log_user = User.objects.get(username=request.session.get('username'))
    if not pk:
        error_message = '不合法的请求参数!'
        return JsonResponse({'code': 400, 'err': error_message})
    server = get_object_or_404(models.Server, pk=pk)
    server.delete()
    login_event_log(log_user, 25, '资产 {} 删除成功'.format(server.hostname), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_USER_AGENT', None))
    return JsonResponse({"code": 200, 'err': ""})