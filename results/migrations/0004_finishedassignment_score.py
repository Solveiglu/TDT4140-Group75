# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_finishedassignment_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='finishedassignment',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]