# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-28 23:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screening',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema.Event'),
        ),
    ]