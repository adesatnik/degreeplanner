# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quarter', models.CharField(max_length=50, choices=[(b'Autumn', b'Autumn'), (b'Winter', b'Winter'), (b'Spring', b'Spring')])),
                ('year', models.IntegerField()),
                ('index', models.CharField(max_length=50)),
                ('courses', models.ManyToManyField(default=None, to='planner.Course', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=1000)),
                ('number_required', models.IntegerField()),
                ('is_filter', models.BooleanField(default=False)),
                ('filter_string', models.CharField(max_length=500, blank=True)),
                ('class_groups', models.ManyToManyField(to='planner.Requirement', blank=True)),
                ('classes', models.ManyToManyField(to='planner.Course', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(default=None, to='planner.Course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='plan',
            field=models.ForeignKey(default='', to='planner.DegreePlan'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='major',
            name='requirements',
            field=models.ManyToManyField(to='planner.Requirement', blank=True),
        ),
    ]
