# Generated by Django 3.2.5 on 2021-09-19 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TerminalLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64, verbose_name='操作人')),
                ('hostname', models.CharField(max_length=128, verbose_name='主机名')),
                ('ip', models.GenericIPAddressField(verbose_name='主机IP')),
                ('port', models.SmallIntegerField(default=22, verbose_name='端口')),
                ('username', models.CharField(max_length=128, verbose_name='用户名')),
                ('cmd', models.TextField(verbose_name='命令详情')),
                ('address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('useragent', models.CharField(blank=True, max_length=512, null=True, verbose_name='User_Agent')),
                ('start_time', models.DateTimeField(verbose_name='会话开始时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='事件时间')),
            ],
            options={
                'verbose_name': '在线会话日志',
                'verbose_name_plural': '在线会话日志',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='TerminalLogDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res', models.TextField(default='未记录', verbose_name='结果详情')),
                ('terminallog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webssh.terminallog')),
            ],
            options={
                'verbose_name': '在线会话日志结果详情',
                'verbose_name_plural': '在线会话日志结果详情',
            },
        ),
    ]
