from django.db import models


class BusinessUnit(models.Model):
    """
    业务线
    """
    name = models.CharField('业务线', max_length=64, unique=True)
    memo = models.CharField('备注', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = '业务线'

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='机房名称')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = '机房'

    def __str__(self):
        return self.name


class Server(models.Model):
    """
    服务器信息 主机
    """

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name='添加方式')

   # tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    # on_delete 当 主表 记录被删时，不会影响到资产数据表
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='所在机房', on_delete=models.SET_NULL)

    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线', on_delete=models.SET_NULL)

    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )
    # asset_name = models.CharField(max_length=32, unique=True, verbose_name='资产名称')  # 不可重复
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')
    # 基本信息+主板信息+CPU信息
    hostname = models.CharField('主机名', max_length=128, unique=True)
    os_platform = models.CharField('系统', max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)

    sn = models.CharField('SN号', max_length=64, db_index=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)

    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)

    latest_date = models.DateField('最后更新时间', auto_now=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ["-latest_date"]
        verbose_name = '服务器表'
        verbose_name_plural = '服务器表'

    def __str__(self):
        return self.hostname


class Disk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField("插槽位", max_length=8)
    model = models.CharField('磁盘型号', max_length=108)
    capacity = models.FloatField('磁盘容量GB')
    pd_type = models.CharField('磁盘类型', max_length=32)
    # 删除主表数据时 从表数据一并删除 CASCADE
    server = models.ForeignKey(verbose_name='服务器', to='Server', related_name='disk_list',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '硬盘表'

    def __str__(self):
        return self.slot


class NIC(models.Model):
    """
    网卡信息
    """
    name = models.CharField('网卡名字', max_length=128)
    hwaddr = models.CharField('网卡mac地址', max_length=64)
    netmask = models.CharField(max_length=64)
    ipaddrs = models.CharField('ip地址', max_length=256)
    up = models.BooleanField(default=False)
    server = models.ForeignKey('Server', related_name='nic_list', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '网卡表'

    def __str__(self):
        return self.name


class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField('插槽位', max_length=64)
    manufacturer = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64)
    capacity = models.FloatField('容量', null=True, blank=True)
    sn = models.CharField('内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField('速度', max_length=64, null=True, blank=True)

    server = models.ForeignKey('Server', related_name='memory_list', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '内存表'

    def __str__(self):
        return self.slot


class AssetRecord(models.Model):
    """
    资产变更记录
    """
    server = models.ForeignKey('Server', related_name='servers', on_delete=models.CASCADE)
    content = models.TextField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '资产记录表'













