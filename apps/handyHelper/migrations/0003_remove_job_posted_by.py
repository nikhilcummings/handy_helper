# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-19 18:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handyHelper', '0002_auto_20190719_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='posted_by',
        ),
    ]
