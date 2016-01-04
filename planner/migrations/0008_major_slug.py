# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0007_degreeplan_declared_majors'),
    ]

    operations = [
        migrations.AddField(
            model_name='major',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
