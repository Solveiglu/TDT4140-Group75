# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_auto_20170423_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='finishedassignment',
            name='passed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='finishedassignment',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
