# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0004_remove_answer_assignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='passingGrade',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
