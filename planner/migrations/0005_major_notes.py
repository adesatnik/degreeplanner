# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_requirement_filter_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='major',
            name='notes',
            field=models.CharField(max_length=2000, blank=True),
        ),
    ]
