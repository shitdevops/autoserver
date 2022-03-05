# Generated by Django 3.2.7 on 2021-09-23 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_loginlog_event_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginlog',
            name='event_type',
            field=models.SmallIntegerField(choices=[(1, '登陆'), (2, '退出'), (3, '登陆错误'), (4, '修改密码失败'), (5, '修改密码成功'), (6, '添加用户'), (7, '删除用户'), (8, '添加组'), (9, '删除组'), (10, '更新用户'), (11, '更新组'), (12, '添加主机'), (13, '删除主机'), (14, '更新主机'), (15, '添加主机用户'), (16, '删除主机用户'), (17, '更新主机用户'), (18, '添加业务线'), (19, '删除业务线'), (20, '更新业务线'), (21, '添加机房'), (22, '删除机房'), (23, '更新机房')], default=1, verbose_name='事件类型'),
        ),
    ]
