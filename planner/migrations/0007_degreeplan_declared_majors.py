# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_requirement_filter_blacklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='degreeplan',
            name='declared_majors',
            field=models.ManyToManyField(to='planner.Major', blank=True),
        ),
    ]
