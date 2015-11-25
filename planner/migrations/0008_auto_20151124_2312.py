# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0007_auto_20151124_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='filter_string',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='requirement',
            name='is_filter',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='major',
            name='requirements',
            field=models.ManyToManyField(to='planner.Requirement', blank=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='name',
            field=models.CharField(unique=True, max_length=1000),
        ),
    ]
