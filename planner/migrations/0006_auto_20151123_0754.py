# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_auto_20151121_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirement2',
            name='class_groups',
        ),
        migrations.RemoveField(
            model_name='requirement2',
            name='requirement_ptr',
        ),
        migrations.AddField(
            model_name='requirement',
            name='class_groups',
            field=models.ManyToManyField(related_name='_class_groups_+', to='planner.Requirement', blank=True),
        ),
        migrations.DeleteModel(
            name='Requirement2',
        ),
    ]
