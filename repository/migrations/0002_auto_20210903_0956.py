# Generated by Django 3.2.5 on 2021-09-03 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memory',
            name='server',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='memory_list', to='repository.server'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='idc',
            name='floor',
            field=models.IntegerField(verbose_name='楼层'),
        ),
    ]