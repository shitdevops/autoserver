# Generated by Django 3.2.5 on 2021-09-11 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_server_business_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='c_day',
            field=models.DateField(auto_now=True, null=True, verbose_name='创建日期'),
        ),
    ]
