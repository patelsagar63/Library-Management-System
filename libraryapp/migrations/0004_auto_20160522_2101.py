# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 21:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0003_auto_20160522_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libitem',
            name='num_chkout',
        ),
        migrations.RemoveField(
            model_name='libuser',
            name='age',
        ),
    ]
