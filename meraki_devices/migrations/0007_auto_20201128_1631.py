# Generated by Django 2.1.9 on 2020-11-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meraki_devices', '0006_auto_20201128_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conectivityinfodevice',
            name='meraki',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='conectivityinfodevice',
            name='vehicle',
            field=models.CharField(max_length=254),
        ),
    ]
