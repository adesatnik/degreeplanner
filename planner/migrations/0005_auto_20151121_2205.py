# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_auto_20151121_2204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirement2',
            name='lel',
        ),
        migrations.AddField(
            model_name='requirement2',
            name='class_groups',
            field=models.ManyToManyField(related_name='_class_groups_+', to='planner.Requirement2', blank=True),
        ),
    ]
