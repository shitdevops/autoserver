# _*_ coding:utf-8 _*_
# By:赵先宇
from repository import models


def process_basic(info):
    server_dict = {}
    server_dict.update(info['basic']['data'])
    server_dict.update(info['main_board']['data'])
    server_dict.update(info['cpu']['data'])
    # 获取要修改的主机
    old_hostname = info.get('hostname') if info.get('hostname') else info['basic']['data']['hostname']
    hostname = info['basic']['data']['hostname']
    server_list = models.Server.objects.filter(hostname=old_hostname)
    server_list.update(**server_dict)
    server = models.Server.objects.get(hostname=hostname)
    return server


def process_disk(info, server):
    disk_info = info['disk']['data']  # 汇报的数据
    disk_query = models.Disk.objects.filter(server=server)  # 数据库中的硬盘数据
    # print(disk_query) <QuerySet [<Disk: 0>, <Disk: 1>, <Disk: 2>, <Disk: 3>]>

    disk_slot_set = set(disk_info)  # 汇报的槽位的集合
    disk_db_slot_set = {disk.slot for disk in disk_query}  # 数据库中的槽位的集合

    # print('1', disk_slot_set) {'4', '5', '0', '2', '1', '3'}
    # print('2', disk_db_slot_set) {'0', '2', '1', '3'}

    # 新增槽位的集合 差 运算 {'5', '4'} 多出来的
    disk_add_set = disk_slot_set - disk_db_slot_set
    # 删除槽位的集合 set() 要删除的没有 没有多出来的数据
    disk_del_set = disk_db_slot_set - disk_slot_set
    # 更新槽位的集合 交集 {'0', '2', '1', '3'} 两个都有的
    disk_update_set = disk_db_slot_set & disk_slot_set

    # 新增硬盘
    disk_add_list = []
    add_record_list = []
    for slot in disk_add_set:
        row_dict = disk_info[slot]

        tpl_list = []  # ['插槽位 : 0', '磁盘类型 : SAS', '磁盘容量GB : 279.396', '磁盘型号 : SEAGATE ST300MM0006     LS08S0K2B5NV']
        for name, value in row_dict.items():
            verbose_name = models.Disk._meta.get_field(name).verbose_name
            tpl_list.append("{} :{}".format(verbose_name, value))

        content = "新增硬盘,信息如下: {}".format(';'.join(tpl_list))
        add_record_list.append(models.AssetRecord(server=server, content=content))  # 变更记录的对象
        disk_add_list.append(models.Disk(**row_dict, server=server))  # 硬盘的对象

    if disk_add_list:
        models.Disk.objects.bulk_create(disk_add_list)
        models.AssetRecord.objects.bulk_create(add_record_list)

    # 更新硬盘
    update_record_list = []
    for slot in disk_update_set:
        row_dict = disk_info[slot]  # 新值
        disk_obj = models.Disk.objects.filter(server=server, slot=slot).first()  # 原硬盘对象

        tpl_list = []  # '容量 由 100 变更成 200
        update_dict = {}  # 字段名： 要更新的值
        for name, value in row_dict.items():
            old_value = getattr(disk_obj, name)

            if value != str(old_value):
                update_dict[name] = value
                verbose_name = models.Disk._meta.get_field(name).verbose_name
                tpl_str = "{}由{}变成{}".format(verbose_name, old_value, value)
                tpl_list.append(tpl_str)
        if tpl_list:
            content = "硬盘更新-槽位{}变更信息如下：{}".format(slot, ';'.join(tpl_list))
            record_obj = models.AssetRecord(server=server, content=content)
            update_record_list.append(record_obj)

            models.Disk.objects.filter(server=server, slot=slot).update(**update_dict)  # 变换字段的更新
    if update_record_list:
        models.AssetRecord.objects.bulk_create(update_record_list)

    # 删除硬盘
    if disk_del_set:
        models.Disk.objects.filter(server=server, slot__in=disk_del_set).delete()
        models.AssetRecord.objects.create(server=server, content="删除硬盘: 槽位{}的硬盘被移除了".format(','.join(disk_del_set)))

    """
    原  0 1 2 8
    新 0 1 2 3 4 5

    8 删除
    0 1 2 更新
    3 4 5 新增
    """


def process_memory(info, server):
    memory_info = info['memory']['data']

    memory_query = models.Memory.objects.filter(server=server)

    memory_slot_set = set(memory_info)
    memory_db_slot_set = {memory.slot for memory in memory_query}

    # 新增槽位
    memory_add_set = memory_slot_set - memory_db_slot_set
    # 删除槽位
    memory_del_set = memory_db_slot_set - memory_slot_set
    # 更新槽位
    memory_update_set = memory_db_slot_set & memory_slot_set

    # 新增内存
    memory_add_list = []
    for slot, row_dict in memory_info.items():
        if slot in memory_add_set:
            memory_add_list.append(models.Memory(**row_dict, server=server))
        # 更新
        elif slot in memory_update_set:
            models.Memory.objects.filter(server=server, slot=slot).update(**row_dict)

    if memory_add_list:
        models.Memory.objects.bulk_create(memory_add_list)

    # 删除内存
    if memory_del_set:
        models.Memory.objects.filter(server=server, slot__in=memory_del_set).delete()


def process_nic(info, server):
    nic_info = info['nic']['data']
    nic_query = models.NIC.objects.filter(server=server)

    nic_name_set = set(nic_info)  # 网卡名 {'eth0'}
    nic_db_name_set = {nic.name for nic in nic_query}

    # 新增网卡的集合
    nic_add_set = nic_name_set - nic_db_name_set
    # 删除网卡的集合
    nic_del_set = nic_db_name_set - nic_name_set
    # 更新网卡
    nic_update_set = nic_db_name_set & nic_name_set

    # 新增网卡
    nic_add_list = []
    for name, row_dict in nic_info.items():
        # print(name, row_dict) eth0 {'up': True, 'hwaddr': '00:1c:42:a5:57:7a', 'ipaddrs': '10.211.55.4', 'netmask': '255.255.255.0'}
        if name in nic_add_set:
            # row_dict['name'] = name
            nic_add_list.append(models.NIC(**row_dict, name=name, server=server))

        # 更新
        elif name in nic_update_set:
            models.NIC.objects.filter(server=server, name=name).update(**row_dict)

        if nic_add_list:
            models.NIC.objects.bulk_create(nic_add_list)

        # 删除网卡
        if nic_del_set:
            models.NIC.objects.filter(server=server, name__in=nic_del_set).delete()
