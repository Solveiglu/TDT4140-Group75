# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 18:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0007_auto_20170423_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finishedassignment',
            name='passed',
        ),
        migrations.RemoveField(
            model_name='finishedassignment',
            name='score',
        ),
    ]
