# Generated by Django 3.2.9 on 2022-02-27 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_remoteuserbindhost_host_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remoteuserbindhost',
            name='ex_ip',
        ),
    ]