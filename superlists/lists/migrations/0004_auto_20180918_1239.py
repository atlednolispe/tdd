# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-18 12:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20180903_1319'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('list', 'text')]),
        ),
    ]