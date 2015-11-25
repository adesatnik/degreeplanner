# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0008_auto_20151124_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cross_listings',
            field=models.ManyToManyField(related_name='_cross_listings_+', to='planner.Course'),
        ),
        migrations.AlterField(
            model_name='quarter',
            name='courses',
            field=models.ManyToManyField(default=None, to='planner.Course', blank=True),
        ),
    ]
