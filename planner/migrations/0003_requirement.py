# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_auto_20151120_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000)),
                ('number_required', models.IntegerField()),
                ('class_groups', models.ManyToManyField(related_name='_class_groups_+', to='planner.Requirement')),
                ('classes', models.ManyToManyField(to='planner.Course')),
            ],
        ),
    ]
