import json
import traceback
import shutil
import re
from ansible.playbook.play import Play  # 用于执行 Ad-hoc 的核心类，即ansible相关模块，命令行的ansible -m方式
from ansible.executor.task_queue_manager import TaskQueueManager  # ansible 底层用到的任务队列管理器
from ansible.executor.playbook_executor import PlaybookExecutor  # 执行 playbook 的核心类，即命令行的ansible-playbook *.yml
from ansible import constants as C  # 用于获取ansible内置的一些常量
from multiprocessing import cpu_count
from ansible import context  # 上下文管理器，他就是用来接收 ImmutableDict 的示例对象
from ansible.module_utils.common.collections import ImmutableDict  # 用于自定制一些选项
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host # 单台主机类
from ansible.plugins.callback import CallbackBase # 回调基类，处理ansible的成功失败信息，这部分对于二次开发自定义可以做比较多的自定义
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


class ModuleCallbackModule(CallbackBase):
    """
    回调函数
    """
    def __init__(self, group, cmd=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group
        self.cmd = cmd
        self.message = dict()

    def v2_runner_on_unreachable(self, result):
        if 'msg' in result._result:
            print('aaaa')
            data = '<code style="color: #FF0000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：不可达 | 状态码：{rc} >> \n{stdout}</code>'.format(
                host=result._host.name, rc=result._result.get('rc'),
                ip=result._host.host_data['ip'],
                user=result._host.host_data['username'],
                cmd=self.cmd,
                stdout=result._result.get('msg').strip()
            )
        else:
            print('bbbbb')
            data = '<code style="color: #FF0000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：不可达 >> \n{stdout}</code>'.format(
                host=result._host.name,
                ip=result._host.host_data['ip'],
                user=result._host.host_data['username'],
                cmd=self.cmd,
                stdout=json.dumps(result._result, indent=4, ensure_ascii=False))
        self.message['status'] = 0
        self.message['message'] = data
        message = json.dumps(self.message)
        async_to_sync(channel_layer.group_send)(self.group, {
            "type": "send.message",
            "text": message,
        })

    def v2_runner_on_ok(self, result, *args, **kwargs):
        if 'rc' in result._result and 'stdout' in result._result:
            if result._result['stderr']:
                print('ccc')
                data = '<code style="color: #008000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：成功 | 状态码：{rc} >> \n{stdout}\n{stderr}</code>'.format(
                    host=result._host.name, rc=result._result.get('rc'),
                    ip=result._host.host_data['ip'],
                    user=result._host.host_data['username'],
                    cmd=self.cmd,
                    stdout=result._result.get('stdout').strip(),
                    stderr=result._result.get('stderr').strip())
            else:
                print('ddd')
                data = '<code style="color: #008000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：成功 | 状态码：{rc} >> \n{stdout}</code>'.format(
                    host=result._host.name, rc=result._result.get('rc'),
                    ip=result._host.host_data['ip'],
                    user=result._host.host_data['username'],
                    cmd=self.cmd,
                    stdout=result._result.get('stdout').strip())
        elif 'results' in result._result and 'rc' in result._result:
            print('eee')
            data = '<code style="color: #008000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：成功 | 状态码：{rc} >> \n{stdout}</code>'.format(
                host=result._host.name, rc=result._result.get('rc'),
                ip=result._host.host_data['ip'],
                user=result._host.host_data['username'],
                cmd=self.cmd,
                stdout=result._result.get('results')[0].strip())
        elif 'module_stdout' in result._result and 'rc' in result._result:
            print('ffff')
            data = '<code style="color: #008000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：成功 | 状态码：{rc} >> \n{stdout}</code>'.format(
                host=result._host.name, rc=result._result.get('rc'),
                ip=result._host.host_data['ip'],
                user=result._host.host_data['username'],
                cmd=self.cmd,
                stdout=result._result.get('module_stdout').strip())
        else:
            print('gggg')
            data = '<code style="color: #008000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：成功 >> \n{stdout}</code>'.format(
                host=result._host.name,
                ip=result._host.host_data['ip'],
                user=result._host.host_data['username'],
                cmd=self.cmd,
                stdout=json.dumps(result._result, indent=4, ensure_ascii=False))
        self.message['status'] = 0
        self.message['message'] = data
        message = json.dumps(self.message)
        async_to_sync(channel_layer.group_send)(self.group, {
            "type": "send.message",
            "text": message,
        })

    def v2_runner_on_failed(self, result, *args, **kwargs):
        if 'stderr' in result._result:
            if result._result['stdout']:
                print('aaa')
                data = '<code style="color: #FF0000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：失败 | 状态码：{rc} >> \n{stdout}\n{stderr}</code>'.format(
                    host=result._host.name,
                    rc=result._result.get('rc'),
                    ip=result._host.host_data['ip'],
                    user=result._host.host_data['username'],
                    cmd=self.cmd,
                    stdout=result._result.get('stdout').strip(),
                    stderr=result._result.get('stderr').strip())
            else:
                print('bbb')
                data = '<code style="color: #FF0000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：失败 | 状态码：{rc} >> \n{stderr}</code>'.format(
                    host=result._host.name,
                    rc=result._result.get('rc'),
                    ip=result._host.host_data['ip'],
                    user=result._host.host_data['username'],
                    cmd=self.cmd,
                    stderr=result._result.get('stderr').strip())
        elif 'module_stdout' in result._result:
            print('ccc')
            data = '<code style="color: #FF0000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：失败 | 状态码：{rc} >> \n{stdout}</code>'.format(
                host=result._host.name,
                rc=result._result.get('rc'),
                ip=result._host.host_data['ip'],
                user=result._host.host_data['username'],
                cmd=self.cmd,
                stdout=result._result.get('module_stdout').strip())
        else:
            print(result._result)
            data = '<code style="color: #FF0000">主机：{host}_{ip}_{user} | 命令： {cmd} | 状态：失败 >> \n{stdout}</code>'.format(
                host=result._host.name,
                ip=result._host.host_data['ip'],
                user=result._host.host_data['username'],
                cmd=self.cmd,
                stdout=json.dumps(result._result, indent=4, ensure_ascii=False))
        self.message['status'] = 0
        self.message['message'] = data
        message = json.dumps(self.message)
        async_to_sync(channel_layer.group_send)(self.group, {
            "type": "send.message",
            "text": message,
        })

    def v2_playbook_on_no_hosts_matched(self):
        self.message['status'] = 0
        self.message['message'] = '<code style="color: #FF0000">skipping: No match hosts.</code>'
        message = json.dumps(self.message)
        async_to_sync(channel_layer.group_send)(self.group, {
            "type": "send.message",
            "text": message,
        })


class BaseHost(Host):
    """
    处理单个主机
    """
    def __init__(self, host_data):
        self.host_data = host_data
        hostname = host_data.get('hostname') or host_data.get('ip')
        port = host_data.get('port') or 22
        super().__init__(hostname, port)
        self.__set_required_variables()
        self.__set_extra_variables()

    def __set_required_variables(self):
        host_data = self.host_data
        self.set_variable('ansible_host', host_data['ip'])
        self.set_variable('ansible_port', host_data['port'])

        if host_data.get('username'):
            self.set_variable('ansible_user', host_data['username'])

        # 添加密码和秘钥
        if host_data.get('password'):
            self.set_variable('ansible_ssh_pass', host_data['password'])
        if host_data.get('private_key'):
            self.set_variable('ansible_ssh_private_key_file', host_data['private_key'])

        # 添加beceom支持
        become = host_data.get('become', False)
        if become:
            self.set_variable('ansible_become', True)
            self.set_variable('ansible_become_method', become.get('method', 'sudo'))
            self.set_variable('ansible_become_user', become.get('user', 'root'))
        else:
            self.set_variable('ansible_become', False)

    def __set_extra_variables(self):
        for k, v in self.host_data.get('vars', {}).items():
            self.set_variable(k, v)

    def __repr__(self):
        return self.name


class BaseInventory(InventoryManager):
    """
    生成Ansible inventory对象的
    """
    loader_class = DataLoader
    variable_manager_class = VariableManager
    host_manager_class = BaseHost

    def __init__(self, host_list=None):
        if host_list is None:
            host_list = []
        self.host_list = host_list
        assert isinstance(host_list, list)
        self.loader = self.loader_class()
        self.variable_manager = self.variable_manager_class()
        super().__init__(self.loader)

    def get_groups(self):
        return self._inventory.groups

    def get_group(self, name):
        return self._inventory.groups.get(name, None)

    def parse_sources(self, cache=False):
        group_all = self.get_group('all')
        ungrouped = self.get_group('ungrouped')

        for host_data in self.host_list:
            print(host_data)
            host = self.host_manager_class(host_data=host_data)
            self.hosts[host_data['hostname']] = host
            groups_data = host_data.get('groups')
            if groups_data:
                for group_name in groups_data:
                    group = self.get_group(group_name)
                    if group is None:
                        self.add_group(group_name)
                        group = self.get_group(group_name)
                    group.add_host(host)
            else:
                ungrouped.add_host(host)
            group_all.add_host(host)


class AnsibleAPI:
    def __init__(self, check=False, remote_user='root', private_key_file=None, forks=cpu_count(),
                 extra_vars=None, dynamic_inventory=None, callback=None):
        """
        可以选择性的针对业务场景在初始化中加入用户定义的参数
        """
        # 运行前检查，即命令行的-C
        self.check = check
        # key登陆文件
        self.private_key_file = private_key_file
        # 并发连接数
        self.forks = forks
        # 远端登陆用户
        self.remote_user = remote_user
        # 数据解析器
        self.loader = DataLoader()
        # 必须有此参数，假如通过了公钥信任，可以为空dict
        self.passwords = {}
        # 回调结果
        self.results_callback = callback
        # 组和主机相关，处理动态资产
        self.dynamic_inventory = dynamic_inventory
        # 变量管理器
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.dynamic_inventory)
        self.variable_manager._extra_vars = extra_vars if extra_vars is not None else {}
        # 自定义选项的初始化
        self.__init_options()

    def __init_options(self):
        """
        自定义选项，不用默认值的话可以加入到__init__的参数中
        """
        # constants里面可以找到这些参数，ImmutableDict代替了较老的版本的nametuple的方式
        context.CLIARGS = ImmutableDict(
            connection='smart',
            remote_user=self.remote_user,
            ack_pass=None,
            sudo=True,
            sudo_user='root',
            ask_sudo_pass=False,
            module_path=None,
            become=True,
            become_method='sudo',
            become_user='root',
            check=self.check,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None,
            diff=True,
            subset=None,
            timeout=15,
            private_key_file=self.private_key_file,
            host_key_checking=False,
            forks=self.forks,
            ssh_common_args='-o StrictHostKeyChecking=no',
            ssh_extra_args='-o StrictHostKeyChecking=no',
            verbosity=0,
            start_at_task=None,
        )

    def run_module(self, module_name, module_args, hosts='all'):
        """
        运行 module
        """
        play_source = dict(
            name='Ansible Run Module',
            hosts=hosts,
            gather_facts='no',
            tasks=[
                {'action': {'module': module_name, 'args': module_args}},
            ]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.dynamic_inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
            )
            tqm.run(play)
            # self.result_row = self.results_callback.result_row
        except Exception:
            print(traceback.format_exc())
        finally:
            # try:
            #     message = dict()
            #     message['status'] = 0
            #     message['message'] = '执行关闭'
            #     message = json.dumps(message)
            #     async_to_sync(channel_layer.group_send)(self.group, {
            #         "type": "send.message",
            #         "text": message,
            #     })
            # except:
            #     pass
            if tqm is not None:
                tqm.cleanup()
            # 这个临时目录会在 ~/.ansible/tmp/ 目录下
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def run_cmd(self, cmds, hosts='all', group=None):
        """
        运行命令有三种 raw 、command 、shell
        1.command 模块不是调用的shell的指令，所以没有bash的环境变量
        2.raw很多地方和shell类似，更多的地方建议使用shell和command模块。
        3.但是如果是使用老版本python，需要用到raw，又或者是客户端是路由器，因为没有安装python模块，那就需要使用raw模块了
        """
        module_name = 'shell'
        self.run_module(module_name, cmds, hosts)
        if group:
            message = dict()
            message['status'] = 0
            message['message'] = '执行完毕...'
            message = json.dumps(message)
            async_to_sync(channel_layer.group_send)(group, {
                "type": "close.channel",
                "text": message,
            })