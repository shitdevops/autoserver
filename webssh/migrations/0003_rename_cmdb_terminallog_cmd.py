# Generated by Django 3.2.5 on 2021-09-19 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webssh', '0002_rename_cmd_terminallog_cmdb'),
    ]

    operations = [
        migrations.RenameField(
            model_name='terminallog',
            old_name='cmdb',
            new_name='cmd',
        ),
    ]
