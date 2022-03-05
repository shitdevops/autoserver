from django.db.models import Q
from django.shortcuts import render, HttpResponse, get_object_or_404
from user.tool import login_required
from .models import RemoteUser, RemoteUserBindHost, HostGroup
from user.tool import admin_required
from user.models import User, Group
from django.http import JsonResponse


# Create your views here.


@login_required
def host_lists(request):
    if request.session['is_superuser']:
        hosts = RemoteUserBindHost.objects.all()
    else:
        hosts = RemoteUserBindHost.objects.filter(
            Q(user__username=request.session['username']) | Q(group__user__username=request.session['username'])
        ).distinct()
    return render(request, 'host_lists.html', locals())


@login_required
def host_detail(request, host_id):
    host = get_object_or_404(RemoteUserBindHost, pk=host_id)
    return render(request, 'host_detail.html', locals())


@login_required
@admin_required
def host_add(request):
    env_choices = (
        (1, '正式环境'),
        (2, '测试环境'),
    )
    all_users = RemoteUser.objects.all()
    return render(request, 'host_add.html', locals())


@login_required

def host_edit(request, host_id):
    env_choices = (
        (1, '正式环境'),
        (2, '测试环境'),
    )
    host = get_object_or_404(RemoteUserBindHost, pk=host_id)
    other_users = RemoteUser.objects.exclude(pk=host.remote_user_id).exclude(
        remoteuserbindhost__int_ip=host.int_ip,
        remoteuserbindhost__port=host.port
    )
    return render(request, 'host_edit.html', locals())


@admin_required
@login_required
def host_users(request):
    h_users = RemoteUser.objects.all()
    return render(request, 'host_users.html', locals())


@login_required
@admin_required
def user_add(request):
    return render(request, 'user_add.html', locals())


@login_required
@admin_required
def user_detail(request, user_id):
    user = get_object_or_404(RemoteUser, pk=user_id)
    return render(request, 'user_detail.html', locals())


@login_required
@admin_required
def user_edit(request, user_id):
    user = get_object_or_404(RemoteUser, pk=user_id)
    return render(request, 'user_edit.html', locals())


@login_required
def host_groups(request):
    user = User.objects.get(id=int(request.session.get('userid')))
    groups = HostGroup.objects.filter(user=user)
    print(groups)
    for group in groups:
        if request.session['is_superuser']:
            group.hosts = RemoteUserBindHost.objects.filter(
                Q(host_group__id=group.id),
            ).distinct()
        else:
            group.hosts = RemoteUserBindHost.objects.filter(
                Q(user__username=request.session['username']) | Q(group__user__username=request.session['username']),
                Q(host_group__id=group.id),
            ).distinct()
    return render(request, 'host_groups.html', locals())


@login_required
def host_groups_detail(request, groups_id):
    user = User.objects.get(id=int(request.session.get('userid')))
    group = get_object_or_404(HostGroup, pk=groups_id, user=user)

    if request.session['is_superuser']:
        group.hosts = RemoteUserBindHost.objects.filter(
            Q(host_group__id=group.id),
        ).distinct()
    else:
        group.hosts = RemoteUserBindHost.objects.filter(
            Q(user__username=request.session['username']) | Q(group__user__username=request.session['username']),
            Q(host_group__id=group.id),

        ).distinct()
    return render(request, 'host_group_detail.html', locals())


@login_required
def host_groups_edit(request, group_id):
    user = User.objects.get(id=int(request.session.get('userid')))
    group = get_object_or_404(HostGroup, pk=group_id, user=user)
    if request.session['is_superuser']:
        group.hosts = RemoteUserBindHost.objects.filter(
            Q(host_group__id=group.id),
        ).distinct()
    else:
        group.hosts = RemoteUserBindHost.objects.filter(
            Q(user__username=request.session['username']) | Q(group__user__username=request.session['username']),
            Q(host_group__id=group.id),
        ).distinct()

    if request.session['is_superuser']:
        other_hosts = RemoteUserBindHost.objects.filter(
            ~Q(host_group__id=group_id),
        ).distinct()
    else:
        other_hosts = RemoteUserBindHost.objects.filter(
            Q(user__username=request.session['username']) | Q(group__user__username=request.session['username']),
            ~Q(host_group__id=group_id),
        ).distinct()
    print('11' ,other_hosts)
    return render(request, 'host_group_edit.html', locals())


@login_required
def host_groups_add(request):
    if request.session['is_superuser']:
        all_hosts = RemoteUserBindHost.objects.all()
    else:
        all_hosts = RemoteUserBindHost.objects.filter(
            Q(user__username=request.session['username']) | Q(group__user__username=request.session['username'])
        ).distinct()
    return render(request, 'host_group_add.html', locals())
