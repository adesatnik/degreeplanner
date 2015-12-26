# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_major_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='filter_blacklist',
            field=models.ManyToManyField(related_name='requirement_filter_blacklist', to='planner.Course', blank=True),
        ),
    ]
