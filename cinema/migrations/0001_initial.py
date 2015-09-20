# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=60, serialize=False, primary_key=True)),
                ('slug', models.SlugField(max_length=65, unique=True, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=80)),
                ('slug', models.SlugField(max_length=140, unique=True, blank=True, null=True)),
                ('start_day', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_day', models.DateField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(help_text='Geographic location of event, i.e. Austin, Texas', max_length=50, default='', blank=True)),
            ],
            options={
                'get_latest_by': 'start_day',
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ('-start_day', '-end_day', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(max_length=140, unique=True, blank=True, null=True)),
                ('synopsis', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('languages', django.contrib.postgres.fields.ArrayField(default=list, base_field=models.CharField(max_length=30), blank=True, size=None)),
                ('year', models.PositiveIntegerField(help_text='Release year', blank=True, null=True)),
                ('runtime', models.IntegerField(help_text='Film runtime, in whole minutes', blank=True, null=True)),
                ('related_urls', django.contrib.postgres.fields.ArrayField(default=list, base_field=models.URLField(), blank=True, size=None)),
            ],
            options={
                'verbose_name': 'Film',
                'verbose_name_plural': 'Films',
                'ordering': ('title', '-year'),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50, default='', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('location', models.CharField(help_text='Location of film screening', max_length=120, default='', blank=True)),
                ('event', models.ForeignKey(to='cinema.Event')),
                ('film', models.ForeignKey(to='cinema.Film')),
            ],
            options={
                'get_latest_by': 'start_time',
                'verbose_name': 'Screening',
                'verbose_name_plural': 'Screenings',
            },
        ),
        migrations.AddField(
            model_name='film',
            name='actors',
            field=models.ManyToManyField(to='cinema.Person', related_name='acted_in', blank=True),
        ),
        migrations.AddField(
            model_name='film',
            name='countries',
            field=models.ManyToManyField(to='cinema.Country'),
        ),
        migrations.AddField(
            model_name='film',
            name='directors',
            field=models.ManyToManyField(help_text='Usually one person, but can accomodate multiple directors', to='cinema.Person', related_name='directed', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='films',
            field=models.ManyToManyField(to='cinema.Film', related_name='shown_at'),
        ),
    ]
