# Generated by Django 3.2.5 on 2021-09-11 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_alter_tag_c_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='c_day',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建日期'),
        ),
    ]
