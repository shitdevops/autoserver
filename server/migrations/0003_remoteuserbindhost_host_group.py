# Generated by Django 3.2.7 on 2021-11-03 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_hostgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='remoteuserbindhost',
            name='host_group',
            field=models.ManyToManyField(blank=True, to='server.HostGroup', verbose_name='主机组'),
        ),
    ]