# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20170322_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='checknum',
            field=models.IntegerField(),
        ),
    ]