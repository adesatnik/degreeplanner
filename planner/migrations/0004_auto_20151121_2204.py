# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_requirement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement2',
            fields=[
                ('requirement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='planner.Requirement')),
                ('lel', models.CharField(max_length=12)),
            ],
            bases=('planner.requirement',),
        ),
        migrations.RemoveField(
            model_name='requirement',
            name='class_groups',
        ),
        migrations.AlterField(
            model_name='requirement',
            name='classes',
            field=models.ManyToManyField(to='planner.Course', blank=True),
        ),
    ]
