# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-11 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_auto_20160828_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='films',
            field=models.ManyToManyField(blank=True, related_name='shown_at', to='cinema.Film'),
        ),
    ]
