# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_delete_modelodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='filter_display',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
