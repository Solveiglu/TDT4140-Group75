# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-17 12:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_auto_20170407_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AnsweredInAssignment', to='assignments.Assignment'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='assignmentName',
            field=models.CharField(default='oving', max_length=75),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
