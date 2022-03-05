import json
import time
import traceback

from server.models import RemoteUserBindHost
from django.db.models import Q
from .tasks import task_run_cmd
from django.conf import settings
from channels.generic.websocket import WebsocketConsumer
from util.tool import gen_rand_char
from asgiref.sync import async_to_sync
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    session_exipry_time = settings.CUSTOM_SESSION_EXIPRY_TIME
except Exception:
    session_exipry_time = 60 * 15


class Cmd(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = 'session_' + gen_rand_char()
        self.session = dict()
        self.message = dict()

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name) # 加入组
        print(self.channel_name, self.group)
        self.session = self.scope.get('session', dict())
        if not self.session.get('is_login', None): # 未登录直接断开websocket连接
            self.message['status'] = 1
            self.message['message'] = '未登录'
            message = json.dumps(self.message)
            async_to_sync(self.channel_layer.group_send)(self.group, {
                'type': 'close.channel',
                'text': message,
            })

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name) # 退出组
        except Exception:
            print(traceback.format_exc())

    def receive(self, text_data=None, bytes_data=None):
        data = dict()
        try:
            data = json.loads(text_data)
        except Exception:
            self.message['status'] = 1
            self.message['message'] = '提交的数据格式错误'
            message = json.dumps(self.message)
            async_to_sync(self.channel_layer.group_send)(self.group, {
                "type": "close.channel",
                "text": message,
            })
        if data.get('hosts', None) and data.get('cmd', None):
            print(data.get('cmd'))
            if self.session.get('is_superuser', None):
                hosts = RemoteUserBindHost.objects.filter(
                    Q(id__in=data['hosts'].split(',')),
                )
            else:
                hosts = RemoteUserBindHost.objects.filter(
                    Q(user__username=self.session['username']) | Q(
                        group__user__username=self.session['username']),
                    Q(id__in=data['hosts'].split(',')),
                )
            if not hosts:
                self.message['status'] = 1
                self.message['message'] = '未找到主机'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })

            ansible_hosts = list()
            for host in hosts:
                hostinfo = dict()
                hostinfo['id'] = host.id
                hostinfo['hostname'] = host.hostname
                hostinfo['ip'] = host.int_ip
                hostinfo['port'] = host.port
                hostinfo['username'] = host.remote_user.username
                hostinfo['password'] = host.remote_user.password
                if host.remote_user.enabled:
                    hostinfo['superusername'] = host.remote_user.superusername
                    hostinfo['superpassword'] = host.remote_user.superpassword
                else:
                    hostinfo['superusername'] = None
                ansible_hosts.append(hostinfo)
            for i in ansible_hosts:
                print(i)
            task_run_cmd(
                hosts=ansible_hosts, group=self.group,
                cmd=data['cmd'], is_superuser=self.session.get('is_superuser', False)
            )  # 执行

        else:
            self.message['status'] = 1
            self.message['message'] = '提交的数据格式错误'
            message = json.dumps(self.message)
            async_to_sync(self.channel_layer.group_send)(self.group, {
                "type": "close.channel",
                "text": message,
            })

    def send_message(self, data):
        try:
            self.send(data['text'])
        except Exception:
            print(traceback.format_exc())

    def close_channel(self, data):
        try:
            self.send(data['text'])
            time.sleep(0.3)
            self.close()
        except Exception:
            print(traceback.format_exc())

