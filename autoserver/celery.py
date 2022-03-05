from __future__ import absolute_import, unicode_literals
from celery import Celery, platforms
from django.conf import settings
import os

# 为celery程序设置默认的Django设置模块。
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'autoserver.settings')

# 注册Celery的APP
app = Celery('autoserver')

# 绑定配置文件
#app.config_from_object('django.conf.settings', namespace='CELERY')
app.config_from_object ('django.conf:settings')
# celery不能root用户启动解决
platforms.C_FORCE_ROOT = True
# 自动发现各个app下的tasks.py文件
#app.autodiscover_tasks()
app.autodiscover_tasks (lambda :settings.INSTALLED_APPS)