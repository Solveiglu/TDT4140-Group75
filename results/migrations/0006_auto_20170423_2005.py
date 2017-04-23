# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 18:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('results', '0005_merge_20170423_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionresult',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionresult',
            name='user',
        ),
        migrations.RemoveField(
            model_name='finishedassignment',
            name='passed',
        ),
        migrations.RemoveField(
            model_name='finishedassignment',
            name='score',
        ),
        migrations.AddField(
            model_name='finishedassignment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='QuestionResult',
        ),
    ]
