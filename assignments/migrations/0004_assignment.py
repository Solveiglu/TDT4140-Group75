# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0003_auto_20170321_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignmentName', models.CharField(max_length=75)),
                ('deadline', models.DateTimeField()),
                ('questions', models.ManyToManyField(to='assignments.Question')),
            ],
        ),
    ]
