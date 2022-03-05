from django.db import models


# Create your models here.
class HostGroup(models.Model):
    group_name = models.CharField(max_length=128, verbose_name='组名')
    # 当用户删除时 关联的主机组也删除
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='关联用户')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-create_time']
        verbose_name = '主机组'
        verbose_name_plural = '主机组'
        unique_together = ('group_name', 'user')  # 同一用户下 主机组必须唯一

    def __str__(self):
        return self.group_name


class RemoteUser(models.Model):
    """
    名称唯一，用户名可以重复，不同主机登陆用户名相同，密码不同
    """
    name = models.CharField(unique=True, max_length=128, verbose_name="名称")
    username = models.CharField(max_length=128, verbose_name="用户名")
    password = models.CharField(max_length=512, verbose_name="密码")
    enabled = models.BooleanField(default=False, verbose_name='登陆后是否su跳转超级用户')
    superusername = models.CharField(max_length=128, blank=True, null=True, verbose_name="超级用户")
    superpassword = models.CharField(max_length=512, blank=True, null=True, verbose_name="超级密码")
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField('添加时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "主机账户"
        verbose_name_plural = "主机账户"


class RemoteUserBindHost(models.Model):
    ENV_CHOICES = (
        (1, '正式环境'),
        (2, '测试环境'),
    )
    hostname = models.CharField(max_length=128, unique=True, verbose_name='主机名')
    int_ip = models.GenericIPAddressField(verbose_name='主机IP')  # 做了ip映射，ip可能重复，ip:port 不会重复
    #ex_ip = models.GenericIPAddressField(verbose_name='公网IP', blank=True, null=True)
    env = models.SmallIntegerField(default=1, choices=ENV_CHOICES, verbose_name='环境')
    host_group = models.ManyToManyField('HostGroup', blank=True, verbose_name='主机组')
    port = models.SmallIntegerField(default=22, verbose_name='端口')
    release = models.CharField(max_length=255, default='CentOS', verbose_name='系统/型号')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    # on_delete 当 RemoteUser 记录被删时，阻止其操作
    remote_user = models.ForeignKey('RemoteUser', blank=True, null=True, on_delete=models.PROTECT)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField('添加时间', auto_now_add=True)

    def __str__(self):
        return self.hostname

    class Meta:
        ordering = ["-create_time"]
        verbose_name = '远程主机'
        verbose_name_plural = '远程主机'
        unique_together = ('int_ip', 'port', 'remote_user')
        # 一个用户下，只能绑定同一个主机一次，不能一个用户下绑定两个相同主机
