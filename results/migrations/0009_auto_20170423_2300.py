# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 21:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0008_auto_20170423_2050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finishedassignment',
            old_name='answer',
            new_name='answers',
        ),
    ]
