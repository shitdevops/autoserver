# Generated by Django 3.2.7 on 2021-09-25 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0011_remove_server_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memory',
            name='slot',
            field=models.CharField(max_length=64, verbose_name='插槽位'),
        ),
    ]