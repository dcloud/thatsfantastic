# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 20:40
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_auto_20160911_1935'),
    ]

    operations = [
        TrigramExtension(),
    ]
