# Generated by Django 3.2.7 on 2022-01-15 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0012_alter_memory_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='asset_name',
        ),
    ]