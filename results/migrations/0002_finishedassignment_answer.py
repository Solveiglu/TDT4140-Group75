# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='finishedassignment',
            name='answer',
            field=models.ManyToManyField(related_name='answersToAssignment', to='assignments.Answer'),
        ),
    ]