from django.db.models import Q
from django.urls import reverse

from user.tool import login_required, admin_required
from repository import models
from django.shortcuts import render, get_object_or_404, redirect


@login_required
def dashboard(request):
    obj = models.Server.objects.all()
    total = models.Server.objects.count()
    upline = models.Server.objects.filter(status=0).count()
    offline = models.Server.objects.filter(status=1).count()
    unknown = models.Server.objects.filter(status=2).count()
    breakdown = models.Server.objects.filter(status=3).count()
    backup = models.Server.objects.filter(status=4).count()
    up_rate = round(upline / total * 100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)
    return render(request, 'assets/dashboard.html', locals())


@login_required
def server(request):
    servers = models.Server.objects.all()
    bus_list = models.BusinessUnit.objects.all()
    idc_list = models.IDC.objects.all()
    return render(request, 'assets/server.html', locals())


@login_required
def server_record(request, asset_id):
    obj = models.AssetRecord.objects.filter(server_id=asset_id).order_by('-create_at')
    return render(request, 'assets/server_record.html', locals())


@login_required
@admin_required
def server_edit(request, asset_id):
    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )
    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )
    asset = get_object_or_404(models.Server, pk=asset_id)
    # other_business = models.BusinessUnit.objects.exclude(pk=asset.business_unit.id)
    # other_idc = models.IDC.objects.exclude(pk=asset.idc.id)
    other_business = models.BusinessUnit.objects.all()
    other_idc = models.IDC.objects.all()
    # other_tag = models.Tag.objects.filter(  # 多对多反查
    #     ~Q(server__id=asset_id),
    # )

    return render(request, 'assets/server_edit.html', locals())


@login_required
def server_detail(request, asset_id):
    obj = get_object_or_404(models.Server, id=asset_id)
    return render(request, 'assets/server_detail.html', locals())


@login_required
@admin_required
def server_add(request):
    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )
    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )
    all_business = models.BusinessUnit.objects.all()
    all_idc = models.IDC.objects.all()
    # all_tag = models.Tag.objects.all()
    return render(request, 'assets/server_add.html', locals())


@login_required
def business_unit_list(request):
    business_list = models.BusinessUnit.objects.all().order_by('id')
    return render(request, 'assets/business_list.html', locals())


@login_required
@admin_required
def business_edit(request, business_id):
    business = get_object_or_404(models.BusinessUnit, pk=business_id)
    return render(request, 'assets/business_edit.html', locals())


@login_required
def business_detail(request, business_id):
    business = get_object_or_404(models.BusinessUnit, pk=business_id)
    return render(request, 'assets/business_detail.html', locals())


@login_required
@admin_required
def business_add(request):
    return render(request, 'assets/business_add.html', locals())


@login_required
def idc_list(request):
    idc = models.IDC.objects.all()
    return render(request, 'assets/idc_list.html', locals())


@login_required
@admin_required
def idc_detail(request, idc_id):
    idc = get_object_or_404(models.IDC, pk=idc_id)
    return render(request, 'assets/idc_detail.html', locals())


@login_required
@admin_required
def idc_add(request):
    return render(request, 'assets/idc_add.html', locals())


@login_required
@admin_required
def idc_edit(request, idc_id):
    idc = get_object_or_404(models.IDC, pk=idc_id)
    return render(request, 'assets/idc_edit.html', locals())