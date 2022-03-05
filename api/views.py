from repository import models
from api.service import process_basic, process_disk, process_memory, process_nic
from rest_framework.views import APIView
from rest_framework.response import Response
import time, hashlib
from django.conf import settings


def gen_key(ctime):
    key = "{}|{}".format(settings.AUTH_KEY, ctime)
    md5 = hashlib.md5()
    md5.update(key.encode('utf-8'))
    return md5.hexdigest()


SIGN_RECORD = {}
"""
    API验证：
        动态 key|时间戳 -> md5加密
        限制时间
        只能使用一次 
"""


class AuthAPI(APIView):
    # 重写dispatch方法来自定义处理请求
    def dispatch(self, request, *args, **kwargs):
        ret = {'status': True, 'msg': '嘿嘿'}

        key = request.GET.get('key')
        ctime = request.GET.get('ctime')
        now = time.time()

        sign = gen_key(ctime)

        if float(now) - float(ctime) > 2:
            # 时间长就失效
            ret['status'] = False
            ret['msg'] = 'key失效'
            return Response(ret)

        elif key in SIGN_RECORD:
            # key已经使用过了
            ret['status'] = False
            ret['msg'] = 'key已被使用'
            return Response(ret)

        elif key != sign:
            ret['status'] = False
            ret['msg'] = '校验不通过'
            return Response(ret)
        else:
            # 通过校验
            SIGN_RECORD[key] = now
            # 执行父类的dispatch方法
            return super().dispatch(request, *args, **kwargs)


class Asset(APIView):

    def get(self, request):
        print('get')
        host_list = ['192.168.1.30']  # i for i in range(1, 1000)
        return Response(host_list)

    def post(self, request):
        print('post')
        # ret = json.loads(request.body.decode('utf-8'))
        # print(ret, type(ret))

        response = {'status': True, 'hostname': None, 'error': None}

        info = request.data  # 自动反序列化 提交的数据 自动做解析  Content-Type':'application/json

        # print(type(info))
        info_type = info.get('type')

        if info_type == 'create':
            # 新增资产
            # 新增主机
            server_dict = {}

            basic_info = info['basic']['data']
            board_info = info['main_board']['data']
            cpu_info = info['cpu']['data']
            # 把数据放到一个字典里面
            server_dict.update(basic_info)
            server_dict.update(board_info)
            server_dict.update(cpu_info)

            # print(server_dict)

            server = models.Server.objects.create(**server_dict)
            # print('server', server) 返回的是主机名c2.com
            # 新增硬盘
            disk_info = info['disk']['data']
            disk_obj_list = []
            for i in disk_info.values():
                i['server'] = server  # 关联外键
                # models.Disk(**i)  # 内存的实例化对象
                disk_obj_list.append(models.Disk(**i))
            models.Disk.objects.bulk_create(disk_obj_list)  # 批量创建

            # 新增内存
            memory_info = info['memory']['data']
            memory_obj_list = []
            for i in memory_info.values():
                i['server'] = server  # 关联外键
                # models.Disk(**i)  # 内存的实例化对象
                memory_obj_list.append(models.Memory(**i))
            models.Memory.objects.bulk_create(memory_obj_list)  # 批量创建

            # 新增网卡
            nic_info = info['nic']['data']
            nic_obj_list = []
            for name, i in nic_info.items():
                i['server'] = server  # 关联外键
                i['name'] = name  # 网卡名
                # models.Disk(**i)  # 内存的实例化对象
                nic_obj_list.append(models.NIC(**i))
            models.NIC.objects.bulk_create(nic_obj_list)  # 批量创建

        elif info_type == 'update':
            # 更新资产
            print('update')

            # 更新主机表 CPU 主板 基本信息
            server = process_basic(info)

            # 硬盘变更
            process_disk(info, server)

            #       内存变更
            process_memory(info, server)

            #       网卡变更
            process_nic(info, server)

        elif info_type == 'host_update':
            # 更新主机名+资产
            print('host_update')

            # 更新主机表 CPU 主板 基本信息
            server = process_basic(info)

            # 硬盘变更
            process_disk(info, server)

            #       内存变更
            process_memory(info, server)

            #       网卡变更
            process_nic(info, server)

        response['hostname'] = info['basic']['data']['hostname']
        return Response(response)
