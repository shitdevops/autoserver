from autoserver.celery import app
from util.ansible_api import BaseInventory, ModuleCallbackModule, AnsibleAPI


@app.task()
def task_run_cmd(hosts, group, cmd, is_superuser=False):
    print(hosts)
    host_data = list()
    for host in hosts:
        hostinfo = dict()
        hostinfo['hostname'] = host['hostname']
        hostinfo['ip'] = host['ip']
        hostinfo['port'] = host['port']
        hostinfo['username'] = host['username']
        hostinfo['password'] = host['password']
        if is_superuser:
            if host['superusername']:
                hostinfo['become'] = {
                    'method': 'su',
                    'user': host['superusername'],
                    'pass': host['superpassword']
                }
        host_data.append(hostinfo)
    print(1111)
    inventory = BaseInventory(host_data)
    print(2222)
    callback = ModuleCallbackModule(group=group, cmd=cmd)
    print(3333)
    ansible_api = AnsibleAPI(
        dynamic_inventory=inventory,
        callback=callback,
    )

    ansible_api.run_cmd(cmds=cmd, hosts='all', group=group)

