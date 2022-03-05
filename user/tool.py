# _*_ coding:utf-8 _*_
# By:赵先宇
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from functools import wraps
import time


try:
    session_exipry_time = settings.CUSTOM_SESSION_EXIPRY_TIME
except BaseException:
    session_exipry_time = 60 * 15


# 登陆装饰器
def login_required(func):
    @wraps(func)    # 保留原函数信息，添加新功能
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_login', None):
            return redirect(reverse('user:login'))
        lasttime = int(request.session.get('lasttime'))
        now = int(time.time())
        if now - lasttime > session_exipry_time:
            return redirect(reverse('user:logout'))
        else:
            request.session['lasttime'] = now
        return func(request, *args, **kwargs)
    return wrapper


# 超管 才能访问的视图装饰器
def admin_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session['is_superuser']:
            #return JsonResponse({'code': 403, 'err': '无权限'})
            return render(request, '403.html')
        return func(request, *args, **kwargs)
    return wrapper