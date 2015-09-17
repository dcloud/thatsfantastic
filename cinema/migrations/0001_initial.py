# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=80)),
                ('slug', models.SlugField(null=True, blank=True, unique=True, max_length=140)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('location', models.CharField(default='', blank=True, help_text='Geographic location of event, i.e. Austin, Texas', max_length=50)),
            ],
            options={
                'verbose_name': 'Event',
                'ordering': ('-start_date', '-end_date', 'title'),
                'verbose_name_plural': 'Events',
                'get_latest_by': 'start_date',
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(null=True, blank=True, unique=True, max_length=140)),
                ('synopsis', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('countries', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=60), default=list, blank=True, help_text='Country names, not standardized', size=None)),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), default=list, blank=True, size=None)),
                ('year', models.PositiveIntegerField(null=True, blank=True, help_text='Release year')),
                ('runtime', models.IntegerField(null=True, blank=True, help_text='Film runtime, in whole minutes')),
                ('related_urls', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), default=list, blank=True, size=None)),
            ],
            options={
                'verbose_name': 'Film',
                'ordering': ('title', '-year'),
                'verbose_name_plural': 'Films',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(default='', blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('location', models.CharField(default='', blank=True, help_text='Location of film screening', max_length=120)),
                ('event', models.ForeignKey(to='cinema.Event')),
                ('film', models.ForeignKey(to='cinema.Film')),
            ],
            options={
                'verbose_name': 'Screening',
                'verbose_name_plural': 'Screenings',
                'get_latest_by': 'start_time',
            },
        ),
        migrations.AddField(
            model_name='film',
            name='actors',
            field=models.ManyToManyField(to='cinema.Person', blank=True, related_name='acted_in'),
        ),
        migrations.AddField(
            model_name='film',
            name='directors',
            field=models.ManyToManyField(to='cinema.Person', blank=True, help_text='Usually one person, but can accomodate multiple directors', related_name='directed'),
        ),
        migrations.AddField(
            model_name='event',
            name='films',
            field=models.ManyToManyField(to='cinema.Film', related_name='shown_at'),
        ),
    ]
