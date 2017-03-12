# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-21 02:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='libitem',
            name='num_chkout',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='libitem',
            name='date_acquired',
            field=models.DateField(default=datetime.date(2016, 5, 21)),
        ),
    ]
